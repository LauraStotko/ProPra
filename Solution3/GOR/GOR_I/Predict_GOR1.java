package Solution3.GOR.GOR_I;

import Solution3.GOR.TrainingMatrices;

import java.util.HashMap;


public class Predict_GOR1 {

    private TrainingMatrices training_matrices;

    public Predict_GOR1(TrainingMatrices training_matrices){
        this.training_matrices = training_matrices;
    }

    public String predictSS(String sequence){
        StringBuilder predictedStructure = new StringBuilder();

        for (int i = 0; i < sequence.length(); i++) {
            char aa = sequence.charAt(i);

            if (i - 8 >= 0 && i + 8 < sequence.length()) {
                String window = sequence.substring(i - 8, i + 8);

                // Berechnung der Wahrscheinlichkeiten für die Strukturklassen H, E und C
                double probabilityH = calculateProbability(window, 'H');
                double probabilityE = calculateProbability(window, 'E');
                double probabilityC = calculateProbability(window, 'C');

                char predictedSS = 'C'; // Standard: Coil
                if (probabilityH > probabilityE && probabilityH > probabilityC) {
                    predictedSS = 'H'; // Alpha-Helix
                } else if (probabilityE > probabilityH && probabilityE > probabilityC) {
                    predictedSS = 'E'; // Beta-Faltblatt
                }

                predictedStructure.append(predictedSS);
            } else {
                // oder '-', noch fragen
                predictedStructure.append('C'); // Standard: Coil
            }
        }
        return predictedStructure.toString();
    }

    private double calculateProbability(String window, char structure){
        return 0.0;
    }



}
