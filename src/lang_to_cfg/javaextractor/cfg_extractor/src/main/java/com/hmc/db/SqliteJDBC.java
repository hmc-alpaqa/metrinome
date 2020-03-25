package com.hmc.db;

import com.hmc.ComOptions;

import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.DriverManager;
import java.sql.Connection;

public class SqliteJDBC
{
    private static Connection conn;
    
    static {
        SqliteJDBC.conn = null;
    }
    
    public static void connect(final String url) {
        try {
            Class.forName("org.sqlite.JDBC");
            SqliteJDBC.conn = DriverManager.getConnection("jdbc:sqlite:/" + url);
        }
        catch (Exception e) {
            System.err.println(e);
            System.exit(1);
        }
    }
    
    public static void close() {
        try {
            if (SqliteJDBC.conn != null) {
                SqliteJDBC.conn.close();
            }
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public static void insertMethod(final String session, final int access, final String owner, final String name, final String description, final String dotfile) {
        try {
            final String sql = "INSERT INTO method (session, access, owner, name, description, dotfile) VALUES(?,?,?,?,?,?)";
            final PreparedStatement stmt = SqliteJDBC.conn.prepareStatement(sql);
            stmt.setString(1, session);
            stmt.setInt(2, access);
            stmt.setString(3, owner);
            stmt.setString(4, name);
            stmt.setString(5, description);
            stmt.setString(6, dotfile);
            stmt.executeUpdate();
            stmt.close();
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public static void updateMethod(final String id, final String col, final String data) {
        try {
            final String sql = "UPDATE method set " + col + "=? WHERE id=?";
            final PreparedStatement stmt = SqliteJDBC.conn.prepareStatement(sql);
            stmt.setString(1, data);
            stmt.setInt(2, Integer.parseInt(id));
            stmt.executeUpdate();
            stmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public static void select(final String id) {
        try {
            final Statement stmt = SqliteJDBC.conn.createStatement();
            final String sql = "SELECT * FROM method WHERE id=" + id + ";";
            final ResultSet rs = stmt.executeQuery(sql);
            if (rs.next()) {
                final String session = rs.getString("session");
                final int access = rs.getInt("access");
                final String owner = rs.getString("owner");
                final String name = rs.getString("name");
                final String description = rs.getString("description");
                final String dotfile = rs.getString("dotfile");
                System.out.println(String.valueOf(session) + ", " + access + ", " + owner + ", " + name + ", " + description + ", " + dotfile);
                ComOptions.USER_SESSION = session;
                ComOptions.M_ACCESS_CODE = access;
                ComOptions.M_OWNER = owner;
                ComOptions.M_NAME = name;
                ComOptions.M_DESCRIPTION = description;
                ComOptions.M_DOTFILE = dotfile;
            }
            rs.close();
            stmt.close();
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
