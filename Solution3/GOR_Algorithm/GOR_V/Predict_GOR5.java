import java.util.HashMap;
import java.util.List;

public class Predict_GOR5 {
    private HashMap<MatrixKey, TrainingMatrices> trainingMatrices;
    private List<ProteinData> proteinData;
    private String gorMethod;
    private GORPrediction gorPrediction;

    public Predict_GOR5(TrainingMatrices training_matrices, List<ProteinData> as) {
        this.trainingMatrices = trainingMatrices;
        this.proteinData = proteinData;
        this.gorMethod = gorMethod;
    }

    private void initializePredictionMethod(TrainingMatrices trainingMatrices) {
        switch (gorMethod) {
            case "GOR1":
                gorPrediction = new Predict_GOR1(training_matrices, as);
                break;
            case "GOR3":

                break;
            case "GOR4":
                // gorPrediction = new Predict_GOR4(trainingMatrices, proteinData);
                break;
            default:
                throw new IllegalArgumentException("Unbekanntes Vorhersagemodell: " + gorMethod);
        }
    }

    // Startet den Vorhersageprozess über das GORPrediction Interface
    public void startPredict() {
        gorPrediction.startPredict();
    }

    // Gibt die verarbeiteten Protein-Daten zurück
    public List<ProteinData> getProteinData() {
        return gorPrediction.getProteinData();
    }
}
