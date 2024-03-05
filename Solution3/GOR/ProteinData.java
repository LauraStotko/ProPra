package Solution3.GOR;

public class ProteinData {

    private String sequence;
    private String structure;
    private String pdb;

    public ProteinData(String sequence, String structure, String pdb) {
        this.sequence = sequence;
        this.structure = structure;
        this.pdb = pdb;
    }

    public char getSS(int index){
        //return secondayr structure of aa at this index
        return structure.charAt(index);
    }

    public String getPdb() {
        return pdb;
    }

    public String getSequence() {
        return sequence;
    }

    public String getStructure() {
        return structure;
    }



}
