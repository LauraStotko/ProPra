package Solution3.ALIGNMENT;

import java.util.List;
import java.util.Map;

public class Recursive {

    Map<String, String> sequences;
    private List<PdbPair> alignments;

    public void checkSequencesForAlignments() {
        for (PdbPair pair : alignments) {
            String sequence1 = sequences.get(pair.getPdbId1());
            String sequence2 = sequences.get(pair.getPdbId2());

            // Check if either sequence is null or empty
            if (sequence1 == null || sequence1.isEmpty() || sequence2 == null || sequence2.isEmpty()) {
                System.out.println("One or both sequences for alignment pair " + pair.getPdbId1() + " and " + pair.getPdbId2() + " are missing or empty.");
            } else {
                // Sequences are present for both PDB IDs
                System.out.println("Sequences found for both " + pair.getPdbId1() + " and " + pair.getPdbId2());
            }
        }
    }


//    public alignSeqs(){
//        if (alignments)
//    }

}
