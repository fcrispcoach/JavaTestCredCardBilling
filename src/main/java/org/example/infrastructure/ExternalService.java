package org.example.infrastructure;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class ExternalService {
    public String callExternalService() {
        String urlString = "http://localhost:8080/external-service";
        try {
            URL url = new URL(urlString);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            Scanner scanner = new Scanner(conn.getInputStream());
            String response = scanner.useDelimiter("\\A").next();
            scanner.close();

            return response;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}