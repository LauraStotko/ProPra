import java.util.HashMap;
import java.util.Map;

public class Q3Score {

    public static Map<Character, Double> calculateQ3Scores(String actualStructure, String predictedStructure) {
        Map<Character, Integer> correctPredictions = new HashMap<>();
        Map<Character, Integer> totalObserved = new HashMap<>();
        correctPredictions.put('H', 0);
        correctPredictions.put('E', 0);
        correctPredictions.put('C', 0);
        totalObserved.put('H', 0);
        totalObserved.put('E', 0);
        totalObserved.put('C', 0);


        int j = 0;
        while (j< predictedStructure.length() && predictedStructure.charAt(j)=='-'){
            j++;
        }
        if(j==predictedStructure.length())
        {
            return null;
        }
        actualStructure=actualStructure.substring(j, actualStructure.length()-j);
        predictedStructure=predictedStructure.substring(j, predictedStructure.length()-j);

        for (int i = 0; i < actualStructure.length(); i++) {
            char actualChar = actualStructure.charAt(i);
            char predictedChar = predictedStructure.charAt(i);

            if (totalObserved.containsKey(actualChar)) {
                totalObserved.put(actualChar, totalObserved.get(actualChar) + 1);
                if (actualChar == predictedChar) {
                    correctPredictions.put(actualChar, correctPredictions.get(actualChar) + 1);
                }
            }
        }

        Map<Character, Double> q3Scores = new HashMap<>();
        for (Character structureType : totalObserved.keySet()) {
            double score = totalObserved.get(structureType) > 0 ?
                    (double) correctPredictions.get(structureType) / totalObserved.get(structureType) * 100.0 :
                    -1.0;
            q3Scores.put(structureType, score);
        }

        return q3Scores;
    }

}

