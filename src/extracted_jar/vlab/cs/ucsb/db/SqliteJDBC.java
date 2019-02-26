package vlab.cs.ucsb.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import vlab.cs.ucsb.ComOptions;

public class SqliteJDBC {

	private static Connection conn = null;
	public static void connect(String url) {
		try {
			Class.forName("org.sqlite.JDBC");
			conn = DriverManager.getConnection("jdbc:sqlite:/" + url);
		} catch (Exception e) {
			System.err.println(e);
			System.exit(1);
		}
	}
	
	public static void close() {
		try {
			if (conn != null) {
				conn.close();
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public static void insertMethod(String session, int access, String owner, String name, String description, String dotfile) {
		try {
			String sql = "INSERT INTO method (session, access, owner, name, description, dotfile) VALUES(?,?,?,?,?,?)";
			PreparedStatement stmt = conn.prepareStatement(sql);
			stmt.setString(1, session);
			stmt.setInt(2, access);
			stmt.setString(3, owner);
			stmt.setString(4, name);
			stmt.setString(5, description);
			stmt.setString(6, dotfile);
			
			int result = stmt.executeUpdate();
			stmt.close();
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			
		}
	}
	
	public static void updateMethod(String id, String col, String data) {
		try {
			String sql = "UPDATE method set " + col + "=? WHERE id=?";
			PreparedStatement stmt = conn.prepareStatement(sql);
			stmt.setString(1, data);
			stmt.setInt(2, Integer.parseInt(id));
			
			int result = stmt.executeUpdate();
			stmt.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public static void select() {
		try {
			Statement stmt = conn.createStatement();
			String sql = "SELECT * FROM method;";
			ResultSet rs = stmt.executeQuery(sql);
			while (rs.next()) {
				String session = rs.getString("session");
				int access = rs.getInt("access");
				String owner = rs.getString("owner");
				String name = rs.getString("name");
				String description = rs.getString("description");
				String dotfile = rs.getString("dotfile");
				
				System.out.println(session + ", " + access + ", " + owner + ", " + name + ", " + description + ", " + dotfile);
			}
			rs.close();
			stmt.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public static boolean select(String id) {
		try {
			Statement stmt = conn.createStatement();
			String sql = "SELECT * FROM method WHERE id=" + id + ";";
			ResultSet rs = stmt.executeQuery(sql);
			if (rs.next()) {
				String session = rs.getString("session");
				int access = rs.getInt("access");
				String owner = rs.getString("owner");
				String name = rs.getString("name");
				String description = rs.getString("description");
				String dotfile = rs.getString("dotfile");
				
				System.out.println(session + ", " + access + ", " + owner + ", " + name + ", " + description + ", " + dotfile);
				ComOptions.USER_SESSION = session;
				ComOptions.M_ACCESS_CODE = access;
				ComOptions.M_OWNER = owner;
				ComOptions.M_NAME = name;
				ComOptions.M_DESCRIPTION = description;
				ComOptions.M_DOTFILE = dotfile;
			}
			rs.close();
			stmt.close();
			return true;
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return false;
	}
	
	
}
