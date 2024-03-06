import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

public class Train_GOR3 {
    //private TrainingMatricesGOR3 training_matrices;
    private HashMap<MatrixKey, TrainingMatrices> training_matrices;
    private List<ProteinData> proteinData;
    final int m = 8;


    public Train_GOR3(String file, String model) {
        this.training_matrices = new HashMap<>();
        initializeMatrices();
        this.proteinData = readSeqlib(file); // Nutzung der geerbten Methode
        train();
        writeMatricesToFile(model);
    }

    private void initializeMatrices(){
        for (Character aa: GORHelper.getAllAa()){
            training_matrices.put(new MatrixKey(null, aa), new TrainingMatrices());
        }
    }

    private void train() {
        for (ProteinData data : this.proteinData) {
            String seq = data.getSequence();
            String ss = data.getStructure();
            for (int index = m; index + m < seq.length(); index++) {
                char structure = ss.charAt(index);
                char aaMiddle = seq.charAt(index);

                if (!GORHelper.containsAA(aaMiddle)) {
                    continue;
                }

                MatrixKey key = new MatrixKey(null, aaMiddle);

                for (int i = 0; i <= 2*m; i++) {
                    int aaIndex = index + (i - m);
                    char aa = seq.charAt(aaIndex);
                    // Update der Matrix für diesen MatrixKey
                    this.training_matrices.get(key).updateMatrix(structure, aa, i);
                }
            }
        }
    }


    public void writeMatricesToFile(String outputModelFilePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputModelFilePath))) {
            writer.write("// Matrix4D");

            for (char aa : GORHelper.getAllAa()) {

                MatrixKey key = new MatrixKey(null, aa);

                TrainingMatrices trainingMatrices = this.training_matrices.get(key);

                for (char structure : GORHelper.getStructures()) {

                    int[][] matrix = trainingMatrices.getMatrix(structure);
                    writer.write(String.format("\n\n=%s,%s=\n\n", aa, structure));
                    writeMatrix(matrix, writer);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Failed to write matrices to file: " + outputModelFilePath, e);
        }
    }

    private void writeMatrix(int[][] matrix, BufferedWriter writer) throws IOException {
        for (char aa : GORHelper.getAllAa()) {

            writer.write(aa + "\t");

            int row = GORHelper.getRowByAa(aa);
            for (int cell : matrix[row]) {
                writer.write(cell + "\t");
            }
            writer.newLine();  // Move to the next line after writing a row
        }
    }

    public List<ProteinData> readSeqlib(String filepath) {
        List<ProteinData> proteinDataList = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
            String line;
            String id = "";
            StringBuilder aaBuilder = new StringBuilder();
            StringBuilder ssBuilder = new StringBuilder();

            while ((line = br.readLine()) != null) {
                if (line.startsWith(">")) {
                    if (!id.isEmpty()) {
                        // Speichern des vorherigen Eintrags
                        ProteinData proteinData = new ProteinData(id, aaBuilder.toString(), ssBuilder.toString());
                        proteinDataList.add(proteinData);

                        // Zurücksetzen der Builder für den nächsten Eintrag
                        aaBuilder.setLength(0);
                        ssBuilder.setLength(0);
                    }
                    // Neues Protein-ID
                    id = line.substring(1);
                } else if (line.startsWith("AS")) {
                    // Aminosäure-Sequenz hinzufügen
                    aaBuilder.append(line.substring(3));
                } else if (line.startsWith("SS")) {
                    // Sekundärstruktur hinzufügen
                    ssBuilder.append(line.substring(3));
                }
            }
            // Letzten Eintrag hinzufügen
            if (!id.isEmpty()) {
                proteinDataList.add(new ProteinData(id, aaBuilder.toString(), ssBuilder.toString()));
            }
        } catch (IOException e) {
            System.out.println("Error reading the file: " + e.getMessage());
        }
        return proteinDataList;
    }
}
