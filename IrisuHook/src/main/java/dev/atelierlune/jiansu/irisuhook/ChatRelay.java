package dev.atelierlune.jiansu.irisuhook;

import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;

public class ChatRelay implements Listener{
    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event){
        Bukkit.broadcastMessage("Player said: %s" + event.getMessage());
    }
}
