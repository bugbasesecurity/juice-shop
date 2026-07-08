package main

import (
	"database/sql"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
)

var db *sql.DB

func adminShell(w http.ResponseWriter, r *http.Request) {
	cmd := r.URL.Query().Get("cmd")
	out, _ := exec.Command("sh", "-c", cmd).CombinedOutput()
	w.Write(out)
}

func proxyFetch(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("url")
	resp, err := http.Get(target)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}

func readInvoice(w http.ResponseWriter, r *http.Request) {
	invoiceID := r.URL.Query().Get("invoice_id")
	rows, _ := db.Query(fmt.Sprintf("SELECT total FROM invoices WHERE id = %s", invoiceID))
	fmt.Fprintf(w, "%v", rows)
}

func readDiskFile(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")
	body, _ := os.ReadFile("/srv/reports/" + name)
	w.Write(body)
}

func main() {
	http.HandleFunc("/admin/shell", adminShell)
	http.HandleFunc("/proxy", proxyFetch)
	http.HandleFunc("/invoice", readInvoice)
	http.HandleFunc("/file", readDiskFile)
	http.ListenAndServe(":8080", nil)
}
