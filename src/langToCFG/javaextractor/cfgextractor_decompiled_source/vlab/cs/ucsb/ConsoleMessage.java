package vlab.cs.ucsb;

import org.apache.commons.lang3.StringUtils;

public class ConsoleMessage
{
    private static final int header_width = 120;
    private static final char header_char = '/';
    private static final char header2_char = '~';
    private static final char header3_char = '-';
    private static final char body_char = '.';
    
    public static void header(final String msg) {
        final String fill = StringUtils.repeat('/', 120);
        final int lwidth = (120 - msg.length()) / 2;
        final String lpad = StringUtils.repeat('/', lwidth);
        int rwidth = 120 - lwidth - msg.length() - 2;
        if (rwidth <= 0) {
            rwidth = 1;
        }
        final String rpad = StringUtils.repeat('/', rwidth);
        System.out.println();
        System.out.println(String.format("%5s%s", " ", fill));
        System.out.println(String.format("%5s%s %s %s", " ", lpad, msg.toUpperCase(), rpad));
        System.out.println(String.format("%5s%s", " ", fill));
        System.out.println();
    }
    
    public static void header2(final String msg) {
        final int lwidth = (120 - msg.length()) / 2;
        final String lpad = StringUtils.repeat('~', lwidth);
        int rwidth = 120 - lwidth - msg.length() - 2;
        if (rwidth <= 0) {
            rwidth = 1;
        }
        final String rpad = StringUtils.repeat('~', rwidth);
        System.out.println(String.format("\n%5s%s %s %s\n", " ", lpad, msg, rpad));
    }
    
    public static void header3(final String msg) {
        final int lwidth = (120 - msg.length()) / 2;
        final String lpad = StringUtils.repeat('-', lwidth);
        int rwidth = 120 - lwidth - msg.length() - 2;
        if (rwidth <= 0) {
            rwidth = 1;
        }
        final String rpad = StringUtils.repeat('-', rwidth);
        System.out.println(String.format("\n%5s%s %s %s\n", " ", lpad, msg, rpad));
    }
    
    public static void body1(final String msg) {
        System.out.println(String.format("\n%12s%s%s", " ", StringUtils.repeat('.', 3), msg));
    }
    
    public static void body1(final String TAG, final String msg) {
        System.out.println(String.format("\n%12s%s%s: %s", " ", StringUtils.repeat('.', 3), TAG, msg));
    }
    
    public static void body2(final String msg) {
        System.out.println(String.format("%12s%s%s", " ", StringUtils.repeat('.', 6), msg));
    }
    
    public static void body2(final String TAG, final String msg) {
        System.out.println(String.format("%12s%s%s: %s", " ", StringUtils.repeat('.', 6), TAG, msg));
    }
    
    public static void body3(final String msg) {
        System.out.println(String.format("%12s%s%s", " ", StringUtils.repeat('.', 9), msg));
    }
    
    public static void warning(final String TAG, final String msg) {
        System.out.println(String.format("\n%12s: %s", "Warning!", msg));
    }
    
    public static void info(final String msg) {
        System.out.println(String.format("\n%5sINFO: %s", " ", msg));
    }
}
