package com.hmc;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.ClassReader;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.RegexFileFilter;

import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import com.hmc.analysis.CFGClassVisitor;


public class Extractor
{

    public static Options buildOptions() {
        // Set the command line options to look for.
        final Options comOptions = new Options();
        comOptions.addOption("p", "package-name", true, "application package name");
        comOptions.addOption("d", "database", true, "database url");
        comOptions.addOption("s", "session", true, "user session identifier");
        comOptions.addOption("m", "method", true, "db id of the method to analyze");
        comOptions.addOption("i", "input-classes", true, "folder of classes to be instrumented");
        comOptions.addOption("o", "output-folder", true, "output graphs");
        comOptions.addOption("h", "help", false, "list available options");

        return comOptions;
    }

    public static void parseOptions(final Options comOptions, final String[] args) {
        // Parse the command line arguments.
        final CommandLineParser comParser = new DefaultParser();
        CommandLine com;
        try {
            com = comParser.parse(comOptions, args);
        }
        catch (final Exception e2) {
            exit(comOptions);
            return;
        }
        if (com.hasOption('h'))
            exit(comOptions);
        if (com.hasOption('i'))
            ComOptions.INPUT_CLASS_FOLDER_PATH = com.getOptionValue('i');
        if (com.hasOption('o'))
            ComOptions.OUTPUT_FOLDER_PATH = com.getOptionValue('o');
        if (com.hasOption('p'))
            ComOptions.PACKAGE_NAME = com.getOptionValue('p');
        if (com.hasOption('s'))
            ComOptions.USER_SESSION = com.getOptionValue('s');
    }

    public static Collection<File> getFiles(File inputPath) {
        System.out.println("Working directory = " + System.getProperty("user.dir"));
        final Collection<File> classFiles;
        if (inputPath.isDirectory()) {
            classFiles = FileUtils.listFiles(
                    inputPath, new RegexFileFilter("[^\\s]+\\.class$"),
                    DirectoryFileFilter.DIRECTORY
            );
        } else {
            classFiles = new ArrayList<>();
            ((ArrayList<File>) classFiles).add(0, inputPath);
        }

        return classFiles;
    }

    public static void main(final String[] args) {
        // Get options from the command line.
        final Options comOptions = buildOptions();
        parseOptions(comOptions, args);

        // inputPath can either be a single file or a directory.
        final File inputPath = new File(ComOptions.INPUT_CLASS_FOLDER_PATH);
        final File instrumentedClassFolder = new File(ComOptions.OUTPUT_FOLDER_PATH);
        info("input classes folder -> " + inputPath);
        info("output folder -> " + instrumentedClassFolder);
        Collection<File> classFiles = getFiles(inputPath);

        // Create CFG for each of the files in the list.
        for (final File classFile : classFiles) {
            try {
            	byte[] byteArray = FileUtils.readFileToByteArray(classFile);
                final ClassReader cr = new ClassReader(byteArray);
                final ClassWriter cw = new ClassWriter(1);
                ClassVisitor cv = new CFGClassVisitor(cw);
                cr.accept(cv, 0);
            }
            catch (final IOException e) {
                System.out.println(e.getMessage());
                System.out.println(e.toString());
                e.printStackTrace();
                System.exit(-1);
            }
        }
    }
    
    private static void exit(final Options options) {
        final HelpFormatter helpFormatter = new HelpFormatter();
        helpFormatter.printHelp("Available command line options", options, true);
        System.exit(0);
    }

    static void info(final String msg) {
        System.out.println(String.format("\n%5sINFO: %s", " ", msg));
    }
}