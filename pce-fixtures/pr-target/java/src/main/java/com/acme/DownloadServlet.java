package com.acme;

import java.io.File;
import java.io.FileInputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DownloadServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        try {
            String name = request.getParameter("file");
            File report = new File("/srv/reports/" + name);
            FileInputStream stream = new FileInputStream(report);
            response.getWriter().write("downloaded " + name);
            response.getOutputStream().write(stream.readAllBytes());
        } catch (Exception error) {
            response.setStatus(404);
        }
    }
}
