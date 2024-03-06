package Solution3.ALIGNMENT;
import org.apache.commons.cli.*;

import java.util.List;
import java.util.Map;

public class Executor {

    private static boolean validateMode(String mode) {
        return "local".equals(mode) || "global".equals(mode) || "freeshift".equals(mode);
    }

    private static boolean validateFormat(String format) {
        return "scores".equals(format) || "ali".equals(format) || "html".equals(format);
    }

    public static void main(String[] args) {
        Options options = defineOptions();
        CommandLineParser cmdParser = new DefaultParser();
        try {
            // Matches the arguments provided by the user against the Options definition and produces a
            // CommandLine object that allows you to query the presence of options and retrieve their argument values
            CommandLine cmd = cmdParser.parse(options, args);

            // Check if the 'go' option is provided; if not, use a default value
            int gapOpenValue = cmd.hasOption("go") ? Integer.parseInt(cmd.getOptionValue("go")) : -12;

            // Check if the 'ge' option is provided; if not, use a default value
            int gapExtendValue = cmd.hasOption("ge") ? Integer.parseInt(cmd.getOptionValue("ge")) : -1;

            // Makes sure that user enters only valid mode argument
            //String mode = cmd.getOptionValue("mode");
            if (!validateMode(cmd.getOptionValue("mode"))) {
                throw new ParseException("Invalid mode selected. Please choose one of: local, global, freeshift.");
            }

            // Makes sure that user enters only valid format argument
            //String format = cmd.getOptionValue("format");
            if (!validateFormat(cmd.getOptionValue("format"))) {
                throw new ParseException("Invalid format selected. Please choose one of: scores, ali, html.");
            }


            // boolean isCheckEnabled = cmd.hasOption("check");
            // boolean isNWEnabled = cmd.hasOption("nw");

            String pairsPath = cmd.getOptionValue("pairs");
            String seqlibPath = cmd.getOptionValue("seqlib");
            String substitutionMatrixPath = cmd.getOptionValue("m");
            InputProcessor ip = new InputProcessor(pairsPath, seqlibPath, substitutionMatrixPath);

            Map<String, String> sequences = ip.getSequences();
            List<PdbPair> alignments = ip.getAlignments();

            NeedlemanWusch nw = new NeedlemanWusch();
            nw.printMatrix();
            nw.backtrack();
            //Recursive recursive = new Recursive(3, -2, gapOpenValue, sequences, alignments);
            //recursive.calculateAlignment();
            //System.out.println(sequences);
            //System.out.println(alignments);


        } catch (ParseException e) {
            System.err.println("Error parsing command line options: " + e.getMessage());
            HelpFormatter formatter = new HelpFormatter();
            formatter.printHelp("java -jar alignment.jar", options, true);
        }
    }

    private static Options defineOptions() {
        Options options = new Options();

        // REQUIRED OPTIONS
        options.addOption(Option.builder("pairs")
                .hasArg()
                .desc("Path to pairs file")
                .required()
                .build());

        options.addOption(Option.builder("seqlib")
                .hasArg()
                .desc("Path to sequence library file")
                .required()
                .build());

        options.addOption(Option.builder("m")
                .hasArg()
                .desc("Path to substitution matrix file")
                .required()
                .build());

        options.addOption(Option.builder("mode")
                .hasArg()
                .desc("Alignment mode (local|global|freeshift)")
                .required()
                .build());

        options.addOption(Option.builder("format")
                .hasArg()
                .desc("Output format (scores|ali|html)")
                .required()
                .build());

        // OPTIONAL OPTIONS
        options.addOption(Option.builder("go")
                .longOpt("gapopen")
                .hasArg() // Indicates that this option requires an argument
                .desc("Set gap open penalty")
                .build());

        options.addOption(Option.builder("ge")
                .longOpt("gapextend")
                .hasArg()
                .desc("Set gap extend penalty")
                .build());

        options.addOption(Option.builder()
                .longOpt("dpmatrices")
                .hasArg()
                .desc("Output directory for dynamic programming matrices")
                .build());

        options.addOption("check", false, "Check flag: to calculate checkscores " +
                "for all alignments and output only incorrect alignments"); // If not present automatically false
        options.addOption("nw", false, "Use NW/SW algorithms"); // If not present automatically false

        return options;
    }

    public void executeAlignment(){

    }

    public void handleOutput(){

    }
}
