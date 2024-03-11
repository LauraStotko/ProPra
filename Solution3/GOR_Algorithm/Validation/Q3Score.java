import java.util.HashMap;
import java.util.Map;

public class Q3Score {

    public static Map<Character, Double> calculateQ3Scores(String actualStructure, String predictedStructure) {
        Map<Character, Integer> correctPredictions = new HashMap<>();
        Map<Character, Integer> totalPredictions = new HashMap<>();
        correctPredictions.put('H', 0);
        correctPredictions.put('E', 0);
        correctPredictions.put('C', 0);
        totalPredictions.put('H', 0);
        totalPredictions.put('E', 0);
        totalPredictions.put('C', 0);

        for (int i = 0; i < actualStructure.length(); i++) {
            char actualChar = actualStructure.charAt(i);
            char predictedChar = predictedStructure.charAt(i);

            if (totalPredictions.containsKey(actualChar)) {
                totalPredictions.put(actualChar, totalPredictions.get(actualChar) + 1);
                if (actualChar == predictedChar) {
                    correctPredictions.put(actualChar, correctPredictions.get(actualChar) + 1);
                }
            }
        }

        Map<Character, Double> q3Scores = new HashMap<>();
        for (Character structureType : totalPredictions.keySet()) {
            double score = totalPredictions.get(structureType) > 0 ?
                    (double) correctPredictions.get(structureType) / totalPredictions.get(structureType) * 100.0 :
                    0.0;
            q3Scores.put(structureType, score);
        }

        return q3Scores;
    }

}
