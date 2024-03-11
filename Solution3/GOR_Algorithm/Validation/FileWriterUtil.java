import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import java.util.*;
import java.util.stream.Collectors;

public class FileWriterUtil {

    public static void generateSummaryReport(String summaryFilePath, List<ProteinData> proteinDataList) throws IOException {
        for (ProteinData protein : proteinDataList) {
            System.out.println("Sequence Length: " + protein.getSequence().length());
            System.out.println("Predicted Structure Length: " + protein.getPredictedSecondaryStructure().length());
        }

        int numberOfProteins = proteinDataList.size();
        int sumOfProteinLengths = proteinDataList.stream()
                .mapToInt(protein -> protein.getStructure().length())
                .sum();
        double meanProteinLength = numberOfProteins > 0 ? (double) sumOfProteinLengths / numberOfProteins : 0;
        int sumOfPredictedPositions = proteinDataList.stream().mapToInt(protein -> protein.getPredictedSecondaryStructure().replace("-","").length()).sum();

        // Sammeln der SOV- und Q3-Scores für jede Kategorie
        Map<Character, List<Double>> q3CategoryScores = new HashMap<>();
        Map<Character, List<Double>> sovCategoryScores = new HashMap<>();
        List<Double> allSOVScores = new ArrayList<>();
        char[] categories = {'H', 'E', 'C'};
        for (char category : categories) {
            q3CategoryScores.put(category, new ArrayList<>());
            sovCategoryScores.put(category, new ArrayList<>());
        }

        for (ProteinData protein : proteinDataList) {
            Map<Character, Double> q3Scores = protein.getQ3Scores();
            Map<Character, Double> sovScores = protein.getSOVScores();
            for (char category : categories) {
                if (q3Scores != null && q3Scores.containsKey(category)) {
                    q3CategoryScores.get(category).add(q3Scores.get(category));
                }
                if (sovScores != null && sovScores.containsKey(category)) {
                    sovCategoryScores.get(category).add(sovScores.get(category));
                    allSOVScores.add(sovScores.get(category)); // Für Gesamtstatistik
                }
            }
        }

        // Berechnung der Gesamtstatistiken über alle Strukturen für SOV-Scores
        Map<String, Double> overallStatistics = calculateStatisticsForStructure(allSOVScores);

        // Berechnung der Statistiken für Q3- und SOV-Scores pro Kategorie
        Map<Character, Map<String, Double>> q3CategoryStatistics = new HashMap<>();
        Map<Character, Map<String, Double>> sovCategoryStatistics = new HashMap<>();
        for (char category : categories) {
            q3CategoryStatistics.put(category, calculateStatisticsForStructure(q3CategoryScores.get(category)));
            sovCategoryStatistics.put(category, calculateStatisticsForStructure(sovCategoryScores.get(category)));
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(summaryFilePath))) {
            writer.write("Statistics for protein validation\n\n");

            writer.write(String.format("Number of Proteins: %d\n", numberOfProteins));
            writer.write(String.format("Mean Protein Length: %.2f\n", meanProteinLength));
            writer.write(String.format("Sum of Protein Lengths: %d\n", sumOfProteinLengths));
            writer.write(String.format("Sum of Predicted Positions: %d\n", sumOfPredictedPositions));

            writer.write("\n\n");


            // Q3-Scores Statistiken
            writer.write("\nQ3 Score Statistics for each category:\n");
            q3CategoryStatistics.forEach((category, stats) -> {
                try {
                    writeStatistics(writer, String.valueOf(category), stats);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });

            // SOV-Scores Statistiken
            writer.write("\n\nSOV Score Statistics for each category:\n");
            writeStatistics(writer, "SOV:", overallStatistics);
            sovCategoryStatistics.forEach((category, stats) -> {
                try {
                    writeStatistics(writer, String.valueOf(category), stats);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        }
    }

    private static Map<String, Double> calculateStatisticsForStructure(List<Double> scores) {
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

    private static void writeStatistics(BufferedWriter writer, String label, Map<String, Double> stats) throws IOException {
        writer.write(String.format("%s - Mean: %.2f, Median: %.2f, Std Dev: %.2f, Min: %.2f, Max: %.2f, Quantil_5: %.2f, Quantil_25: %.2f, Quantil_75: %.2f, Quantil_95: %.2f\n",
                label,
                stats.get("Mean"),
                stats.get("Median"),
                stats.get("Standard Deviation"),
                stats.get("Min"),
                stats.get("Max"),
                stats.get("Quantil_5"),
                stats.get("Quantil_25"),
                stats.get("Quantil_75"),
                stats.get("Quantil_95")));
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

    public static void generateDetailedReport(String detailedFilePath, List<ProteinData> proteinDataList) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(detailedFilePath))) {
            for (ProteinData protein : proteinDataList) {
                double q3Score = calculateTotalQ3Score(protein); 
                double sovScore = calculateTotalSOVScore(protein); 

                Map<Character, Double> q3Scores = protein.getQ3Scores();
                Map<Character, Double> sovScores = protein.getSOVScores();

                // Schreiben des Headers mit Scores
                writer.write(String.format(Locale.US,">%s %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f%n",
                        protein.getPdb(), q3Score, sovScore,
                        q3Scores.get('H'), q3Scores.get('E'), q3Scores.get('C'),
                        sovScores.get('H'), sovScores.get('E'), sovScores.get('C')));

                // Schreiben der Sequenz, vorhergesagten Struktur und tatsächlichen Struktur
                writer.write(protein.getSequence() + "\n");
                writer.write(protein.getPredictedSecondaryStructure() + "\n");
                writer.write(protein.getActualSecondaryStructure() + "\n\n");
            }
        }
    }

    private static double calculateTotalSOVScore(ProteinData protein) {
        Map<Character, Double> sovScores = protein.getSOVScores();
        double totalSOVScore = 0.0;
        int count = 0;

        for (char structureType : new char[] {'H', 'E', 'C'}) {
            if (sovScores.containsKey(structureType)) {
                totalSOVScore += sovScores.get(structureType);
                count++;
            }
        }

        return count > 0 ? totalSOVScore / count : 0.0;
    }

    private static double calculateTotalQ3Score(ProteinData protein) {
        String actualStructure = protein.getActualSecondaryStructure();
        String predictedStructure = protein.getPredictedSecondaryStructure();
        int correctPredictions = 0;

        for (int i = 0; i < actualStructure.length(); i++) {
            if (actualStructure.charAt(i) == predictedStructure.charAt(i)) {
                correctPredictions++;
            }
        }

        return actualStructure.length() > 0 ? (double) correctPredictions / actualStructure.length() * 100.0 : 0.0;
    }


}

