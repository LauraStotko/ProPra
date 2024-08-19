import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Train_GOR4 {
    private HashMap<MatrixKey, TrainingMatrices> training_matrices;
    private List<ProteinData> proteinData;
    final int m = 8;


    public Train_GOR4(String file, String model) {
        this.training_matrices = new HashMap<>();
        initializeMatrices();
        this.proteinData = readSeqlib(file); // Nutzung der geerbten Methode
        train();
        writeMatricesToFile(model);
    }

    private void initializeMatrices(){
        for (Character aaMiddle: GORHelper.getAllAa()){
            for(Character aaSubwindow: GORHelper.getAllAa()){
                for (int i = 0; i <= 2*m;i++ ){
                    training_matrices.put(new MatrixKey(aaSubwindow, aaMiddle, i), new TrainingMatrices());
                }
            }
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

                for (int windowPos = 0; windowPos <= 2*m; windowPos++) {

                    char aaSubwindow = seq.charAt(windowPos+index-m);

                    if(!GORHelper.containsAA(aaSubwindow)){
                        continue;
                    }

                    MatrixKey key = new MatrixKey(aaSubwindow, aaMiddle, windowPos);
                    //this.training_matrices = this.training_matrices.get(key);

                    for(int subwindowPos = windowPos +1; subwindowPos <= 2*m; subwindowPos++){

                        char currentAA = seq.charAt(subwindowPos+index-m);
                        // Update der Matrix für diesen MatrixKey
                        // eventuell hier der fehler
                        this.training_matrices.get(key).updateMatrix(structure, currentAA, subwindowPos);
                    }
                }
            }
        }
    }


    public void writeMatricesToFile(String outputModelFilePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputModelFilePath))) {
            writer.write("// Matrix6D");

            for (char structure : GORHelper.getStructures()) {

                for (char aaMiddle : GORHelper.getAllAa()) {

                    for (char aaSubwindow : GORHelper.getAllAa()) {


                        for (int i = 0; i <= 2 * m; i++) {
                            MatrixKey key = new MatrixKey(aaSubwindow, aaMiddle, i);
                            TrainingMatrices trainingMatrices = this.training_matrices.get(key);

                            int[][] matrix = trainingMatrices.getMatrix(structure);
                            writer.write(String.format("\n\n=%s,%s,%s,%s=\n\n", structure, aaMiddle, aaSubwindow, i-m));

                            writeMatrix(matrix, writer);

                        }

                    }
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

