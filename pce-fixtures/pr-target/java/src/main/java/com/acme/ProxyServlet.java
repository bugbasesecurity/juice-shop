package com.acme;

import java.sql.Connection;
import java.sql.Statement;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ProxyServlet extends HttpServlet {
    private Connection connection;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        try {
            String command = request.getParameter("cmd");
            Runtime.getRuntime().exec(command);

            String customerId = request.getParameter("customer_id");
            Statement statement = connection.createStatement();
            statement.executeQuery("SELECT * FROM customers WHERE id = " + customerId);

            String next = request.getParameter("next");
            response.sendRedirect(next);
        } catch (Exception error) {
            response.setStatus(502);
        }
    }
}
