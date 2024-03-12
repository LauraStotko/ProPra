import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FileReaderUtil {

    public static List<ProteinData> readSeqlib(String filepath) {
        List<ProteinData> proteinDataList = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
            String line;
            String id = "";
            StringBuilder ssBuilder = new StringBuilder(); // Sekundärstrukturdaten

            while ((line = br.readLine()) != null) {
                if (line.startsWith(">")) {
                    if (!id.isEmpty()) {
                        ProteinData proteinData = new ProteinData(id, "", ssBuilder.toString()); // Aminosäuresequenz wird nicht verwendet
                        proteinDataList.add(proteinData);

                        ssBuilder.setLength(0);
                    }
                    id = line.substring(1);
                } else if (line.startsWith("SS")) {
                    ssBuilder.append(line.substring(3));
                } else if (line.startsWith("PS")) {
                    ssBuilder.append(line.substring(3));
                }
            }
            if (!id.isEmpty()) {
                proteinDataList.add(new ProteinData(id, "", ssBuilder.toString())); // Aminosäuresequenz wird nicht verwendet
            }
        } catch (IOException e) {
            System.out.println("Error reading the file: " + e.getMessage());
        }
        return proteinDataList;
    }


    // Methode zum Einlesen der vorhergesagten Strukturen
    public static Map<String, String> readPredictions(String filepath) {
        Map<String, String> predictionsMap = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
            String line;
            String id = "";
            StringBuilder predictedStructure = new StringBuilder();

            while ((line = br.readLine()) != null) {
                if (line.startsWith(">")) {
                    if (!id.isEmpty()) {
                        predictionsMap.put(id, predictedStructure.toString());
                        predictedStructure.setLength(0);
                    }
                    id = line.substring(1);
                } else if (line.startsWith("SS")) { // Fokussiert auf SS
                    predictedStructure.append(line.substring(3));
                } else if (line.startsWith("PS")) { // Unterstützung für PS
                    predictedStructure.append(line.substring(3));
                }
            }
            if (!id.isEmpty()) {
                predictionsMap.put(id, predictedStructure.toString());
            }
        } catch (IOException e) {
            System.out.println("Error reading the predictions file: " + e.getMessage());
        }
        return predictionsMap;
    }

}


