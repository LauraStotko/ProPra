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
        // Define options for command line inputs
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
            protein.calculateAndSetSOVScores(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure());
        }

        calculateStatistics(proteinDataList);

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

    private static void calculateStatistics(List<ProteinData> proteinDataList) {
        // Berechnung für Typ H
        calculateAndPrintStatistics(proteinDataList, 'H');

        // Berechnung für Typ E
        calculateAndPrintStatistics(proteinDataList, 'E');

        // Berechnung für Typ C
        calculateAndPrintStatistics(proteinDataList, 'C');
    }

    private static void calculateAndPrintStatistics(List<ProteinData> proteinDataList, char type) {
        List<Double> scores = proteinDataList.stream()
                .mapToDouble(protein -> {
                    switch (type) {
                        case 'H': return protein.getSovScoreH();
                        case 'E': return protein.getSovScoreE();
                        case 'C': return protein.getSovScoreC();
                        default: return Double.NaN;
                    }
                })
                .boxed()
                .collect(Collectors.toList());

        double mean = scores.stream().mapToDouble(Double::doubleValue).average().orElse(Double.NaN);
        double min = scores.stream().mapToDouble(Double::doubleValue).min().orElse(Double.NaN);
        double max = scores.stream().mapToDouble(Double::doubleValue).max().orElse(Double.NaN);
        double median = calculateMedian(scores);
        double stdDev = calculateStandardDeviation(scores, mean);
    }

    private static double calculateMedian(List<Double> scores) {
        int size = scores.size();
        List<Double> sortedScores = scores.stream().sorted().collect(Collectors.toList());
        if (size % 2 == 0) {
            return (sortedScores.get(size / 2 - 1) + sortedScores.get(size / 2)) / 2.0;
        } else {
            return sortedScores.get(size / 2);
        }
    }

    private static double calculateStandardDeviation(List<Double> scores, double mean) {
        double sum = scores.stream().mapToDouble(score -> Math.pow(score - mean, 2)).sum();
        return Math.sqrt(sum / scores.size());
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

            double sovScore = SOVScore.calculateSOVScore(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure(), 'H'); // Example for 'H'
            Map<Character, Double> sovScores = new HashMap<>();
            sovScores.put('H', sovScore); // Repeat for 'E' and 'C'
            protein.setSOVScores(sovScores);
        }
    }
}


