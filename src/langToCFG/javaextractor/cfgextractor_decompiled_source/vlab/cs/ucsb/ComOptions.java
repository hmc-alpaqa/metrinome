package vlab.cs.ucsb;

public class ComOptions
{
    public static String INPUT_CLASS_FOLDER_PATH;
    public static String OUTPUT_FOLDER_PATH;
    public static String PACKAGE_NAME;
    public static final String CLASS_FILE_REGEX = "[^\\s]+\\.class$";
    public static boolean DB_MODE;
    public static String DB_URL;
    public static boolean SINGLE_METHOD_MODE;
    public static String DB_METHOD_ID;
    public static String USER_SESSION;
    public static int M_ACCESS_CODE;
    public static String M_OWNER;
    public static String M_NAME;
    public static String M_DESCRIPTION;
    public static String M_DOTFILE;
    
    static {
        ComOptions.INPUT_CLASS_FOLDER_PATH = "";
        ComOptions.OUTPUT_FOLDER_PATH = "";
        ComOptions.PACKAGE_NAME = "";
        ComOptions.DB_MODE = false;
        ComOptions.DB_URL = "";
        ComOptions.SINGLE_METHOD_MODE = false;
        ComOptions.DB_METHOD_ID = "";
        ComOptions.USER_SESSION = "";
        ComOptions.M_ACCESS_CODE = 0;
        ComOptions.M_OWNER = "";
        ComOptions.M_NAME = "";
        ComOptions.M_DESCRIPTION = "";
        ComOptions.M_DOTFILE = "";
    }
}
