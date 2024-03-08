import java.util.List;

public interface GORPrediction {
    void startPredict(); // Startet den Vorhersageprozess
    List<ProteinData> getProteinData(); // Gibt die vorhergesagten Protein-Daten zurück
}


