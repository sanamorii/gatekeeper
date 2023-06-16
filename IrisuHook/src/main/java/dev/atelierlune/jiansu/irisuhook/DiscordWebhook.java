package dev.atelierlune.jiansu.irisuhook;

import org.json.*
import org.json.simple.JSONObject;

import javax.net.ssl.HttpsURLConnection;
import java.io.IOException;
import java.net.URL;

public class DiscordWebhook {
    private final String url;
    private String username;
    JSONObject payload;

    public DiscordWebhook(String url){
        this.url = url;
    }

    public boolean execute(String username, String content) throws IOException {
        String JSON = String.format("{\"content\": \"%s\", \"username\":", "yes");

        URL obj = new URL(this.url);
        HttpsURLConnection conn = (HttpsURLConnection) obj.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("User-Agent", "Mozilla/5.0");

    }
}
