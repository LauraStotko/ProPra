import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class GORHelper {

    private static final char[] STRUCTURES = {'C', 'E', 'H'};
    private static final char[] AMINO_ACIDS = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'};

    private final static Map<Character, Integer> mapping2row = Map.ofEntries(
            Map.entry('A', 0),
            Map.entry('C', 1),
            Map.entry('D', 2),
            Map.entry('E', 3),
            Map.entry('F', 4),
            Map.entry('G', 5),
            Map.entry('H', 6),
            Map.entry('I', 7),
            Map.entry('K', 8),
            Map.entry('L', 9),
            Map.entry('M', 10),
            Map.entry('N', 11),
            Map.entry('P', 12),
            Map.entry('Q', 13),
            Map.entry('R', 14),
            Map.entry('S', 15),
            Map.entry('T', 16),
            Map.entry('V', 17),
            Map.entry('W', 18),
            Map.entry('Y', 19)
    );
    
    public final static Map<Integer, Character> rowMapping2aa = Map.ofEntries(
            Map.entry(0, 'A'),
            Map.entry(1, 'C'),
            Map.entry(2, 'D'),
            Map.entry(3, 'E'),
            Map.entry(4, 'F'),
            Map.entry(5, 'G'),
            Map.entry(6, 'H'),
            Map.entry(7, 'I'),
            Map.entry(8, 'K'),
            Map.entry(9, 'L'),
            Map.entry(10, 'M'),
            Map.entry(11, 'N'),
            Map.entry(12, 'P'),
            Map.entry(13, 'Q'),
            Map.entry(14, 'R'),
            Map.entry(15, 'S'),
            Map.entry(16, 'T'),
            Map.entry(17, 'V'),
            Map.entry(18, 'W'),
            Map.entry(19, 'Y')
    );

    public static int getRowByAa(char aa) {
        return mapping2row.get(aa);
    }

    public static char[] getAllAa() {
        return AMINO_ACIDS;
    }

    public static char[] getStructures(){
        return STRUCTURES;
    }

    public static boolean containsAA(char aa){
        return  mapping2row.containsKey(aa);
    }
}
