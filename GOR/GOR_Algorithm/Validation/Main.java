import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class Main {
    public static void main(String[] args) {
        Options options = new Options();
        options.addOption("p", true, "Path to predictions file");
        options.addOption("r", true, "Path to seclib file");
        options.addOption("s", true, "Path to summary file");
        options.addOption("d", true, "Path to detailed file");
        options.addOption("f", true, "Output format (txt)");

        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = null;

        try {
            // Parse the command line arguments
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println("Error parsing command line options: " + e.getMessage());
            System.exit(1);
        }

        String predictionsFilePath = cmd.getOptionValue("p");
        String seclibFilePath = cmd.getOptionValue("r");
        String summaryFilePath = cmd.getOptionValue("s");
        String detailedFilePath = cmd.getOptionValue("d");

        List<ProteinData> proteinDataList = FileReaderUtil.readSeqlib(seclibFilePath);
        Map<String, String> predictionsMap = FileReaderUtil.readPredictions(predictionsFilePath);

        updatePredictions(proteinDataList, predictionsMap);

        // Calculate Q3 and SOV scores for each protein data
        calculateScores(proteinDataList);
        for (ProteinData protein : proteinDataList) {
            if (protein.getPredictedSecondaryStructure() == null){
                continue;
            }
            protein.calculateAndSetSOVScores(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure());
        }

        //calculateStatistics(proteinDataList);

        // Output handling - generate summary and detailed reports
        try {
            FileWriterUtil.generateSummaryReport(summaryFilePath, proteinDataList);
            FileWriterUtil.generateDetailedReport(detailedFilePath, proteinDataList); // Hier die neue Methode aufrufen
        } catch (IOException e) {
            System.out.println("Error generating reports: " + e.getMessage());
            System.exit(1);
        }

        System.out.println("Validation completed successfully.");
    }


    private static void updatePredictions(List<ProteinData> proteinDataList, Map<String, String> predictionsMap) {
        for (ProteinData protein : proteinDataList) {
            String predictedStructure = predictionsMap.get(protein.getPdb());
            if (predictedStructure != null) {
                protein.setPredictedStructure(predictedStructure);
            }
        }
    }

    private static void calculateScores(List<ProteinData> proteinDataList) {
        for (ProteinData protein : proteinDataList) {
            if (protein.getPredictedSecondaryStructure() == null || protein.getPredictedSecondaryStructure().isEmpty()) {
                continue;
            }

            Map<Character, Double> q3Scores = Q3Score.calculateQ3Scores(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure());
            protein.setQ3Scores(q3Scores);

            //double sovScore = SOVScore.calculateSOVScore(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure(), 'H'); // Example for 'H'
            //Map<Character, Double> sovScores = new HashMap<>();
            //sovScores.put('H', sovScore); // Repeat for 'E' and 'C'
            //protein.setSOVScores(sovScores);
        }
    }
}


