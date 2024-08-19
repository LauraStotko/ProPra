package GOR;

public class Postprocessing {

    public static String postprocessing(String structure){
        char[] chars = structure.toCharArray();
        StringBuilder newStructure = new StringBuilder();

        for( int i = 0; i < structure.length(); i++){
            char currentChar = structure.charAt(i);

            if (currentChar == 'H'){
                if (lengthValid(i, structure)){
                    newStructure.append(currentChar);
                } else {
                    newStructure.append(rightStructure(i, structure));
                }
            } else {
                newStructure.append(currentChar);
            }
        }
        return newStructure.toString();

    }

    public static boolean lengthValid(int position, String structure){

        if (position > 0 && position < structure.length() - 1) {
            char prevChar = structure.charAt(position - 1);
            char nextChar = structure.charAt(position + 1);
            return prevChar == 'H' || nextChar == 'H';
        }
        return false;
    }

    public static char rightStructure(int position, String structure){
        char rightStructure = 'C';
        if (position > 0 && position < structure.length() - 1){
            char prevChar = structure.charAt(position - 1);
            char nextChar = structure.charAt(position + 1);

            if (prevChar == nextChar){
                rightStructure = prevChar;
            }
            //maybe also leave the character as it is in the end
            if (prevChar == '-'){
                rightStructure = nextChar;
            }
            if (nextChar == '-'){
                rightStructure = prevChar;
            }
        }
        return rightStructure;
    }

}
