package dev.atelierlune.jiansu.gatekeeper_plugin;

import org.json.*
import org.json.simple.JSONObject;

public class DiscordWebhook {
    private final String url;
    private String username;
    JSONObject payload;

    public DiscordWebhook(String url){
        this.url = url;
    }

    public boolean execute(String username, String content){
        String JSON = String.format("{\"content\": \"%s\", \"username\":");
        this.payload = new JSONObject()
    }
}
