import java.io.File;
import java.io.IOException;
import java.util.Collection;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.PosixParser;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.RegexFileFilter;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;

import vlab.cs.ucsb.ComOptions;
import vlab.cs.ucsb.ConsoleMessage;
import vlab.cs.ucsb.analysis.CFGClassVisitor;
import vlab.cs.ucsb.db.SqliteJDBC;


public class Extractor {

	public static void main(String[] args) {
		Options comOptions = new Options();
		
		comOptions.addOption("p","package-name", true, "application package name");
		comOptions.addOption("d","database", true, "database url");
		
		comOptions.addOption("s", "session", true, "user session identifier");
		comOptions.addOption("m", "method", true, "db id of the method to analyze");
		
		comOptions.addOption("i", "input-classes", true, "folder of classes to be instrumented");
		comOptions.addOption("o", "output-folder", true, "output graphs");
		comOptions.addOption("h", "help", false, "list available options");

		CommandLineParser comParser = new PosixParser();
		CommandLine com = null;
		
		try {
            com = comParser.parse(comOptions, args);
		} catch (Exception e) {
            exit(comOptions, "Available command line options");
		}
    
		if ( com.hasOption('h') ) {
			exit(comOptions, "Available command line options");
		}
		
		if ( com.hasOption('i') ) {
			ComOptions.INPUT_CLASS_FOLDER_PATH = com.getOptionValue('i');
		} else {
//			exit(comOptions, "Missing folder path to the input classes");
		}
		
		if ( com.hasOption('o') ) {
			ComOptions.OUTPUT_FOLDER_PATH = com.getOptionValue('o');
		} else {
//			exit(comOptions, "Missing output folder path for generated graphs");
		}
		
		if ( com.hasOption('p') ) {
			ComOptions.PACKAGE_NAME = com.getOptionValue('p');
		} else {
			
		}
	
		if ( com.hasOption('s') ) {
			ComOptions.USER_SESSION = com.getOptionValue('s');
		} else {
			
		}
		
		if ( com.hasOption('d') ) {
			ComOptions.DB_URL = com.getOptionValue('d');
			ComOptions.DB_MODE = true;
			SqliteJDBC.connect(ComOptions.DB_URL);
		} else {
			
		}
		
		if ( com.hasOption('m') ) {
			ComOptions.DB_METHOD_ID = com.getOptionValue('m');
			ComOptions.SINGLE_METHOD_MODE = true;
			SqliteJDBC.select(ComOptions.DB_METHOD_ID);
		} else {
			
		}
		
		File classFolder = new File(ComOptions.INPUT_CLASS_FOLDER_PATH);
		File instrumentedClassFolder = new File(ComOptions.OUTPUT_FOLDER_PATH);
		
		ConsoleMessage.info("input classes folder -> " + classFolder);
		ConsoleMessage.info("output folder -> " + instrumentedClassFolder);
		
		Collection<File> classFiles = FileUtils.listFiles(classFolder, new RegexFileFilter(ComOptions.CLASS_FILE_REGEX), DirectoryFileFilter.DIRECTORY);

		for (File classFile : classFiles) {
			try {
				byte[] inBytes = FileUtils.readFileToByteArray(classFile);
				
				ClassReader cr = new ClassReader(inBytes);
				
				if (ComOptions.DB_MODE) {
					if ( !ComOptions.SINGLE_METHOD_MODE) {
						ClassVisitor cv = null;
						ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
						cv = new CFGClassVisitor(cw);
						cr.accept(cv, 0);
					} else if (cr.getClassName().equals(ComOptions.M_OWNER)) {
						ClassVisitor cv = null;
						ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
						cv = new CFGClassVisitor(cw);
						cr.accept(cv, 0);
						break;
					}
				} else {
					ClassVisitor cv = null;
					ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
					cv = new CFGClassVisitor(cw);
					cr.accept(cv, 0);
				}
				
				
//				byte[] outBytes = cw.toByteArray();
//				File instrumentedClassFile = new File(classFile.getPath().replace(classFolder.getPath(), instrumentedClassFolder.getPath()));
//				FileUtils.writeByteArrayToFile(instrumentedClassFile, outBytes);				
			} catch (IOException e) {
				e.printStackTrace();
				System.exit(-1);
			}
		}
		
		SqliteJDBC.close();
	}
	
	public static void exit(Options options, String message) {
        HelpFormatter helpFormatter = new HelpFormatter();
        helpFormatter.printHelp( message, options, true);
        System.exit(0);
	}

}
