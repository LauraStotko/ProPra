package GOR.GOR;

import java.util.HashMap;

public class TrainingMatrices {

    private HashMap<Character, Integer> mapping;
    private int [][] E;
    private int [][] C;
    private int [][] H;

    int windowSize = 17;
    int totalAA = 20;

    public TrainingMatrices(){
        this.mapping = new HashMap<>();
        aaMapping();
        this.E = new int[totalAA][windowSize];
        this.H = new int[totalAA][windowSize];
        this.C = new int[totalAA][windowSize];

    }

    private void aaMapping(){
        this.mapping.put('A', 0);
        this.mapping.put('R', 1);
        this.mapping.put('N', 2);
        this.mapping.put('D', 3);
        this.mapping.put('C', 4);
        this.mapping.put('E', 5);
        this.mapping.put('Q', 6);
        this.mapping.put('G', 7);
        this.mapping.put('H', 8);
        this.mapping.put('I', 9);
        this.mapping.put('L', 10);
        this.mapping.put('K', 11);
        this.mapping.put('M', 12);
        this.mapping.put('F', 13);
        this.mapping.put('P', 14);
        this.mapping.put('S', 15);
        this.mapping.put('T', 16);
        this.mapping.put('W', 17);
        this.mapping.put('Y', 18);
        this.mapping.put('V', 19);
    }

    public void updateMatrix(char structure, char aa, int position){
        // index is where the aa is
        int index = this.mapping.get(aa);
        if (structure == 'E'){
            this.E[index][position] += 1;
        } else if (structure == 'H'){
            this.H[index][position] += 1;
        } else {
            this.C[index][position] += 1;
        }
    }

    public int[][] getMatrix(char structure){
        if (structure == 'E'){
            return this.E;
        } else if (structure == 'H'){
            return this.H;
        } else {
            return this.C;
        }
    }

    public int[][] getC() {
        return C;
    }

    public int[][] getE() {
        return E;
    }

    public int[][] getH() {
        return H;
    }

    public HashMap<Character, Integer> getMapping() {
        return mapping;
    }
}
