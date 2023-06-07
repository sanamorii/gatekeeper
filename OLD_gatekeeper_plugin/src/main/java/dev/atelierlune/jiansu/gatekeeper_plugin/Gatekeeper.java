package dev.atelierlune.jiansu.gatekeeper_plugin;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.Async;

public final class Gatekeeper extends JavaPlugin {

    DiscordWebhook webhook;

    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(new ChatLogger(), this);
    }



    @Override
    public void onDisable() {
    }
}
