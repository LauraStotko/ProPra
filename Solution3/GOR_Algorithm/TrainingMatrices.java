import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

public class TrainingMatrices {


    private HashMap<Character, int[][]> matrices; // Geändert von einzelnen Arrays zu einer Hashmap

    int windowSize = 17;
    int totalAA = 20;

    public TrainingMatrices(){
        this.matrices = new HashMap<>(); // Initialisierung der Hashmap
        this.matrices.put('E', new int[totalAA][windowSize]);
        this.matrices.put('H', new int[totalAA][windowSize]);
        this.matrices.put('C', new int[totalAA][windowSize]);
    }

    public int[][] getMatrix(char structure){
        return matrices.get(structure);
    }

    public double calculateProbability(int position, char structure, char aa){

        // get row index for this aa
        // prüfen ob überhaupt existoert
        if (GORHelper.containsAA(aa)) {
            int row = GORHelper.getRowByAa(aa);
            double valueE = this.matrices.get('E')[row][position];
            double valueC = this.matrices.get('C')[row][position];
            double valueH = this.matrices.get('H')[row][position];

            double numerator = this.matrices.get(structure)[row][position];
            double denominator = (structure == 'E' ? (valueC + valueH) : (structure == 'H' ? (valueC + valueE) : (valueE + valueH)));

            return Math.log(numerator / denominator);
        } else {
            return -1;
        }
    }

    public void fillMatrices(String model){
        try (BufferedReader br = new BufferedReader(new FileReader(model))) {
            String line;
            char structure = 'C';

            while ((line = br.readLine()) != null) {
                if(line.startsWith("//") || line.isEmpty()|| line.equals("\t")){
                    continue;
                }
                if (line.startsWith("=")) {
                    // Struktur folgt nach =
                    structure = line.charAt(1);
                    continue;
                }
                // Teile enthalten Spalten der Matrix
                String[] parts = line.trim().split("\t");
                // Der erste Index der Zeile ist aa
                char aa = line.charAt(0);
                if (!GORHelper.containsAA(aa)) continue; // Sicherstellen, dass aa gültig ist
                int row = GORHelper.getRowByAa(aa);

                for (int i = 0; i < parts.length - 1; i++) { // Erster Eintrag (Aminosäure-Code)
                    // Die Zeile befüllen
                    this.matrices.get(structure)[row][i] = Integer.parseInt(parts[i + 1]);
                }
            }

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public HashMap<Character, int[][]> getMatrices() {
        return matrices;
    }


    public void updateMatrix(char structure,char aa, int position) {
        // Zugriff auf die Matrix basierend auf der Struktur und Aminosäure
        if (GORHelper.containsAA(aa)) {
            int row = GORHelper.getRowByAa(aa);
            this.matrices.get(structure)[row][position] += 1;
        }
    }

    public int getWindowSize() {
        return windowSize;
    }
}
