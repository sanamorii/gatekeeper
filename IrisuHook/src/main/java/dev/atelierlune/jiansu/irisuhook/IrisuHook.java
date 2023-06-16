package dev.atelierlune.jiansu.irisuhook;

import org.bukkit.Bukkit;
import org.bukkit.entity.EntityType;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.entity.Player;

import java.util.Collection;

public final class IrisuHook extends JavaPlugin {

    @Override
    public void onEnable() {
        // Plugin startup logic
        getServer().getPluginManager().registerEvents(new ChatRelay(), this);
    }

    public static int getPlayerCount(){
        return Bukkit.getServer().getOnlinePlayers().size();
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
