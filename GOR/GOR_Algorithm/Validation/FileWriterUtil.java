import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

public class FileWriterUtil {

    public static void generateSummaryReport(String summaryFilePath, List<ProteinData> proteinDataList) throws IOException {
        int numberOfProteins = proteinDataList.size();
        int sumOfProteinLengths = proteinDataList.stream()
                .mapToInt(protein -> protein.getStructure().length())
                .sum();
        double meanProteinLength = numberOfProteins > 0 ? (double) sumOfProteinLengths / numberOfProteins : 0;
        int sumOfPredictedPositions = proteinDataList.stream().mapToInt(protein -> protein.getPredictedSecondaryStructure().replace("-", "").length()).sum();

        // Sammeln der SOV- und Q3-Scores für jede Kategorie
        Map<Character, List<Double>> q3CategoryScores = new HashMap<>();
        Map<Character, List<Double>> sovCategoryScores = new HashMap<>();
        List<Double> allSOVScores = new ArrayList<>();
        List<Double> allQ3Scores = new ArrayList<>(); // Für Gesamt-Q3-Statistiken
        char[] categories = {'H', 'E', 'C'};
        for (char category : categories) {
            q3CategoryScores.put(category, new ArrayList<>());
            sovCategoryScores.put(category, new ArrayList<>());
        }

        for (ProteinData protein : proteinDataList) {
            Map<Character, Double> q3Scores = protein.getQ3Scores();
            Map<Character, Double> sovScores = protein.getSOVScores();
            double totalQ3Score = calculateTotalQ3Score(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure());
            allQ3Scores.add(totalQ3Score); // Hinzufügen des Gesamt-Q3-Scores zur Liste
            double totalSOVScore = calculateTotalSOVScore(protein);
            allSOVScores.add(totalSOVScore);
            for (char category : categories) {
                if (q3Scores != null && q3Scores.containsKey(category)) {
                    q3CategoryScores.get(category).add(q3Scores.get(category));
                }
                if (sovScores != null && sovScores.containsKey(category)) {
                    sovCategoryScores.get(category).add(sovScores.get(category));
                    //allSOVScores.add(sovScores.get(category)); // Für Gesamtstatistik
                }
            }
        }

        // Berechnung der Gesamtstatistiken über alle Strukturen für SOV-Scores
        Map<String, Double> overallSOVStatistics = calculateStatisticsForStructure(allSOVScores);
        // Berechnung der Gesamtstatistiken über alle Strukturen für Q3-Scores
        Map<String, Double> overallQ3Statistics = calculateStatisticsForStructure(allQ3Scores);

        // Berechnung der Statistiken für Q3- und SOV-Scores pro Kategorie
        Map<Character, Map<String, Double>> q3CategoryStatistics = new HashMap<>();
        Map<Character, Map<String, Double>> sovCategoryStatistics = new HashMap<>();
        for (char category : categories) {
            q3CategoryStatistics.put(category, calculateStatisticsForStructure(q3CategoryScores.get(category)));
            sovCategoryStatistics.put(category, calculateStatisticsForStructure(sovCategoryScores.get(category)));
        }


        try (BufferedWriter writer = new BufferedWriter(new FileWriter(summaryFilePath))) {
            writer.write("\n");
            writer.write("Statistics for protein validation\n\n");

            String labelFormat = "%-28s";
            String numberFormat = "%7d";
            String doubleFormat = "%7.1f";
            String left = "%5d";

            writer.write(String.format(Locale.US, labelFormat + left + "\n", "Number of Proteins: ", numberOfProteins));
            writer.write(String.format(Locale.US, labelFormat + doubleFormat + "\n", "Mean Protein Length: ", meanProteinLength));
            writer.write(String.format(Locale.US, labelFormat + numberFormat + "\n", "Sum of Protein Length: ", sumOfProteinLengths));
            writer.write(String.format(Locale.US, labelFormat + numberFormat + "\n\n", "Sum of Predicted Positions: ", sumOfPredictedPositions));
            // Q3 Overall
            //writer.write("Q3 :\n");
            writeStatistics(writer, "Q3 :\t", overallQ3Statistics);


            char[] orderedCategories = {'H', 'E', 'C'};
            for (char category : orderedCategories) {
                Map<String, Double> stats = q3CategoryStatistics.get(category);
                if (stats != null) {
                    String label = "Q3_" + category + ":";
                    writeStatistics(writer, label, stats);
                }
            }

            writer.write("\n");
            // SOV Overall
            //writer.write("\nSOV :\n");
            writeStatistics(writer, "SOV :\t", overallSOVStatistics);

            // SOV Categories
            for (char category : orderedCategories) {
                Map<String, Double> stats = q3CategoryStatistics.get(category);
                if (stats != null) {
                    String label = "Q3_" + category + ":";
                    writeStatistics(writer, label, stats);
                }
            }

            writer.flush();
        }
    }


    private static void writeStatistics(BufferedWriter writer, String label, Map<String, Double> stats) throws IOException {
        //String prefix = label.equals("Overall") ? " " : label + ":";

        writer.write(String.format(Locale.US, "%s\tMean:\t%.1f\tDev:\t%.1f\tMin:\t%.1f\tMax:\t%.1f\tMedian:\t%.1f\tQuantil_25:\t%.1f\tQuantil_75:\t%.1f\tQuantil_5:\t%.1f\tQuantil_95:\t%.1f\t\n",
                label,
                stats.getOrDefault("Mean", 0.0),
                stats.getOrDefault("Standard Deviation", 0.0),
                stats.getOrDefault("Min", 0.0),
                stats.getOrDefault("Max", 0.0),
                stats.getOrDefault("Median", 0.0),
                stats.getOrDefault("Quantil_25", 0.0),
                stats.getOrDefault("Quantil_75", 0.0),
                stats.getOrDefault("Quantil_5", 0.0),
                stats.getOrDefault("Quantil_95", 0.0)));
    }


    private static Map<String, Double> calculateStatisticsForStructure(List<Double> scores) {

        scores.removeIf(score -> score == -1);

        Map<String, Double> stats = new HashMap<>();
        if (scores.isEmpty()) {
            stats.put("Mean", Double.NaN);
            stats.put("Median", Double.NaN);
            stats.put("Standard Deviation", Double.NaN);
            stats.put("Min", Double.NaN);
            stats.put("Max", Double.NaN);
            stats.put("Quantil_5", Double.NaN);
            stats.put("Quantil_25", Double.NaN);
            stats.put("Quantil_75", Double.NaN);
            stats.put("Quantil_95", Double.NaN);
            return stats;
        }

        double maxScore = scores.stream().mapToDouble(v -> v).max().orElse(Double.NaN);

        List<Double> sortedScores = scores.stream().sorted().collect(Collectors.toList());
        stats.put("Mean", sortedScores.stream().mapToDouble(d -> d).average().orElse(Double.NaN));
        stats.put("Median", calculateMedian(sortedScores));
        stats.put("Standard Deviation", calculateStandardDeviation(sortedScores, stats.get("Mean")));
        stats.put("Min", sortedScores.get(0));
        stats.put("Max", maxScore);
        stats.put("Quantil_5", calculateQuantile(sortedScores, 0.05));
        stats.put("Quantil_25", calculateQuantile(sortedScores, 0.25));
        stats.put("Quantil_75", calculateQuantile(sortedScores, 0.75));
        stats.put("Quantil_95", calculateQuantile(sortedScores, 0.95));

        return stats;
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

    private static double calculateQuantile(List<Double> scores, double quantile) {
        int index = (int) Math.round(quantile * (scores.size() - 1));
        List<Double> sortedScores = scores.stream().sorted().collect(Collectors.toList());
        return sortedScores.get(index);
    }

    public static String numOrMinus(double number){
        if (number == -1){
            return "-";
        } else {
            return String.format(Locale.US, "%.1f", number);
        }
    }
    public static void generateDetailedReport(String detailedFilePath, List<ProteinData> proteinDataList) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(detailedFilePath))) {
            for (ProteinData protein : proteinDataList) {
                double q3Score = calculateTotalQ3Score(protein.getActualSecondaryStructure(), protein.getPredictedSecondaryStructure());
                double sovScore = calculateTotalSOVScore(protein);

                Map<Character, Double> q3Scores = protein.getQ3Scores();
                Map<Character, Double> sovScores = protein.getSOVScores();

                // Schreiben des Headers mit Scores
                writer.write(String.format(Locale.US,">%s %s %s %s %s %s %s %s %s%n",
                        protein.getPdb(), numOrMinus(q3Score), numOrMinus(sovScore),
                        numOrMinus(q3Scores.get('H')), numOrMinus(q3Scores.get('E')), numOrMinus(q3Scores.get('C')),
                        numOrMinus(sovScores.get('H')), numOrMinus(sovScores.get('E')), numOrMinus(sovScores.get('C'))));

                // Schreiben der Sequenz, vorhergesagten Struktur und tatsächlichen Struktur
                writer.write(protein.getSequence() + "\n");
                writer.write(protein.getPredictedSecondaryStructure() + "\n");
                writer.write(protein.getActualSecondaryStructure() + "\n");
            }
        }
    }

    private static double calculateTotalSOVScore(ProteinData protein) {
        String actualStructure = protein.getActualSecondaryStructure();
        String predictedStructure = protein.getPredictedSecondaryStructure();

        // Berechne individuelle SOV Scores
        double[] sovScoreH = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'H', true);
        double[] sovScoreE = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'E', true);
        double[] sovScoreC = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'C', true);

        double totalLength = sovScoreH[1]+sovScoreE[1]+sovScoreC[1];

        // Berechne den gesamten SOV Score als gewichteten Durchschnitt
        double totalSOVScore = Math.max(sovScoreH[0],0)+Math.max(sovScoreE[0],0)+Math.max(sovScoreC[0],0);

        return 100/totalLength*totalSOVScore;
    }

    public static double calculateTotalQ3Score(String actualStructure, String predictedStructure) {
        int j = 0;
        while (j< predictedStructure.length() && predictedStructure.charAt(j)=='-'){
            j++;
        }
        if(j==predictedStructure.length())
        {
            return -1;
        }
        actualStructure=actualStructure.substring(j, actualStructure.length()-j);
        predictedStructure=predictedStructure.substring(j, predictedStructure.length()-j);
        Map<Character, Integer> correctPredictions = new HashMap<>();
        correctPredictions.put('H', 0);
        correctPredictions.put('E', 0);
        correctPredictions.put('C', 0);

        int totalObservations = actualStructure.length(); // Gesamtzahl der Beobachtungen

        for (int i = 0; i < actualStructure.length(); i++) {
            char actualChar = actualStructure.charAt(i);
            char predictedChar = predictedStructure.charAt(i);

            // Zähle nur, wenn der tatsächliche Char zu einem der Strukturtypen gehört
            if (correctPredictions.containsKey(actualChar)) {
                if (actualChar == predictedChar) {
                    correctPredictions.put(actualChar, correctPredictions.get(actualChar) + 1);
                }
            }
        }

        // Summe aller A_ii (korrekte Vorhersagen über alle Typen)
        int sumCorrectPredictions = correctPredictions.values().stream().mapToInt(Integer::intValue).sum();

        // Berechne den gesamten Q3 Score
        double totalQ3Score = ((double) sumCorrectPredictions / totalObservations) * 100.0;

        return totalQ3Score;
    }
}

