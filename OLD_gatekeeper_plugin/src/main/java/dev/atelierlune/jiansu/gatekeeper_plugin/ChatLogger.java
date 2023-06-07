package dev.atelierlune.jiansu.gatekeeper_plugin;

import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.jetbrains.annotations.Async;

public class ChatLogger implements Listener{
    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event){
        Bukkit.broadcastMessage("Player said: %s" + event.getMessage());
    }
}
