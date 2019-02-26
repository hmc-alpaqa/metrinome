package vlab.cs.ucsb;

import org.apache.commons.lang3.StringUtils;

public class ConsoleMessage {
	private static final int header_width = 120;
    private static final char header_char = '/';
    private static final char header2_char = '~';
    private static final char header3_char = '-';
    private static final char body_char = '.';
    
    
    public static void header(String msg) {
		String fill = StringUtils.repeat(header_char, header_width);
		int lwidth = (int) (header_width - msg.length())/2;
		String lpad = StringUtils.repeat(header_char, lwidth);
		int rwidth = header_width - lwidth - msg.length() - 2;
		if (rwidth <= 0 ) rwidth = 1;
		String rpad = StringUtils.repeat(header_char, rwidth);
		System.out.println();
		System.out.println(String.format("%5s%s", " ", fill));
		System.out.println(String.format("%5s%s %s %s", " ", lpad, msg.toUpperCase(), rpad));
		System.out.println(String.format("%5s%s", " ", fill));
		System.out.println();
    }
    
    public static void header2(String msg) {
        int lwidth = (int) (header_width - msg.length())/2;
        String lpad = StringUtils.repeat(header2_char, lwidth);
        int rwidth = header_width - lwidth - msg.length() - 2;
        if (rwidth <= 0 ) rwidth = 1;
        String rpad = StringUtils.repeat(header2_char, rwidth);
        System.out.println(String.format("\n%5s%s %s %s\n", " ", lpad, msg, rpad));
    }
    
    public static void header3(String msg) {
        int lwidth = (int) (header_width - msg.length())/2;
        String lpad = StringUtils.repeat(header3_char, lwidth);
        int rwidth = header_width - lwidth - msg.length() - 2;
        if (rwidth <= 0 ) rwidth = 1;
        String rpad = StringUtils.repeat(header3_char, rwidth);
        System.out.println(String.format("\n%5s%s %s %s\n", " ", lpad, msg, rpad));
	}
	
	public static void body1(String msg) {
        System.out.println(String.format("\n%12s%s%s", " ", StringUtils.repeat(body_char, 3), msg));
	}
	
	public static void body1(String TAG, String msg) {
        System.out.println(String.format("\n%12s%s%s: %s", " ", StringUtils.repeat(body_char, 3), TAG, msg));
	}
	
	public static void body2(String msg) {
        System.out.println(String.format("%12s%s%s", " ", StringUtils.repeat(body_char, 6), msg));
	}
	
	public static void body2(String TAG, String msg) {
		System.out.println(String.format("%12s%s%s: %s", " ", StringUtils.repeat(body_char, 6), TAG, msg));
	}
	
	public static void body3(String msg) {
        System.out.println(String.format("%12s%s%s", " ", StringUtils.repeat(body_char, 9), msg));
	}
	
	public static void warning(String TAG, String msg) {
        System.out.println(String.format("\n%12s: %s", "Warning!", msg));
	}
	
	public static void info(String msg) {
        System.out.println(String.format("\n%5sINFO: %s", " ", msg));
	}
	
}
