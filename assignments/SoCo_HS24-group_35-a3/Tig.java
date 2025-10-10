import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Patch;
import com.github.difflib.patch.AbstractDelta;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*; // This covers Path, Files, DirectoryStream, etc.
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;


public class Tig{
    public Tig() {
    }

    public Path init(String repoName) throws IOException { //means errors have to be declared
        Path folderPath = Path.of(repoName);

        if(!Files.exists(folderPath)){
            Files.createDirectory(folderPath);
        }

        Path tigPath = folderPath.resolve(".tig");
        if (Files.exists(tigPath)){
            System.out.println("Error " + tigPath + " already exists!\n");
            return null;
        } else {       
            Files.createDirectory(tigPath);
        }
        System.out.println("Repository '" + repoName + "' created.\n");
        return tigPath;
    }

    public void add(String filename) {
        StagedWriter stagedWriter = new StagedWriter(filename);
        try{
            stagedWriter.updateStaged();
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage() + "\n");
        }
    }

    public void commit(String message) {
        Integer commitId = null;
        CurrentDate currentDate = new CurrentDate();
        String date = currentDate.currentDate();

        // Log
        FileCreator fileCreator = new FileCreator();
        fileCreator.createFile("commitLog.json");

        CommitWriter writer = new CommitWriter();
        writer.writeLog(message);

        System.out.println(
            // "DEBUG: commit id: '" + commitId + "'. date: '" + date + "'. message: '" + message + "'.\n"
        );

    }

    public void status() {
        Status s = new Status();
        s.checkStatus();
    }

    public void log(String number) {
        Log log = new Log();
        log.showLog(number);
        
    }

    public String diff(String filename) throws IOException {
        // Find the highest numbered directory in .tig 
        int highestCommitId = DiffStuff.findHighestCommitId();
        // System.out.println("DEBUG: The commit-id we're checking first is: " + highestCommitId);

        
        // Construct the path to fileLocation.json
        Path fileLocationsPath = Paths.get(".tig", String.valueOf(highestCommitId), "fileLocation.json").toAbsolutePath();
        
        // Read and parse the JSON file to 
        String fileLocationsJson = Files.readString(fileLocationsPath, StandardCharsets.UTF_8);
        Map<String, String> jsonMap = StagedWriter.parseJson(fileLocationsJson);
        
        // Find find latest priorversion of file
        for (Map.Entry<String, String> entry : jsonMap.entrySet()) {
            if (entry.getKey().equals(filename)) {
                String version = entry.getValue();
                // System.out.println("DEBUG: The version we should compare to is: " + version);

                Path fileToCompare = Paths.get(".tig", version, filename);
                // System.out.println("DEBUG: Path of file we compare to: " + fileToCompare);

                
                String diffOutput =  DiffStuff.createUnifiedDiff(fileToCompare, Paths.get(filename)); 
                System.out.println(diffOutput);

                return diffOutput;
            }
        }
        
        // If file not found
        throw new FileNotFoundException("File " + filename + " not found in the latest commit");
    } // end of diff method

    public void checkout(String commitId) throws IOException {
        // Define paths
        Path fileLocationsPath = Paths.get(".tig", commitId, "fileLocation.json").toAbsolutePath(); // json path
        Path destDir = Paths.get("").toAbsolutePath(); // Current working directory
        Path commitDir = Paths.get(".tig", commitId).toAbsolutePath(); // commit-id directory  
        // System.out.println("DEBUG: Checking out commit: " + commitId);
        // System.out.println("DEBUG: File locations path: " + fileLocationsPath);
        // System.out.println("DEBUG: Destination directory: " + destDir);
        // System.out.println("DEBUG: Commit directory: " + commitDir);
        // Verify commit-id / directory exists
    if (!Files.exists(commitDir)) {
        throw new IllegalArgumentException("Commit directory does not exist: " + commitDir);
    }
    // Verify fileLocation.json exists

    if (!Files.exists(fileLocationsPath)) {
        throw new IllegalArgumentException("fileLocations.json not found: " + fileLocationsPath);
    }

        // Read and parse the file_location.json
        String fileLocationsJson = Files.readString(fileLocationsPath, StandardCharsets.UTF_8);
        Map<String, String> jsonMap = StagedWriter.parseJson(fileLocationsJson);
        // System.out.println("DEBUG: fileLocationsJson: " + fileLocationsJson);


        // Delete all files in the directory except .tig
        try (Stream<Path> files = Files.list(destDir)) {
            files.forEach(file -> {
                if (Files.isRegularFile(file)) { // Check if it's a file (and not a directory)
                    try {
                        Files.delete(file); // Delete the file
                    } catch (IOException e) {
                        System.err.println("Failed to delete file: " + file + " - " + e.getMessage());
                    }
                }
            });
        }

        // copy committed files to current repo
        for (Map.Entry<String, String> entry : jsonMap.entrySet()) {
            String version = entry.getValue();
            String filename = entry.getKey();
            // System.out.println("DEBUG: filename: " + filename + " commmit-id: " + version );

            Path sourceFile = Paths.get(".tig", version, filename);
            Path destPath = destDir.resolve(filename); //resolve appends the filename to the path

            if (Files.exists(sourceFile)) {
                // System.out.println("DEBUG: sourceFile exists: " + sourceFile);
                Files.copy(sourceFile, destPath, StandardCopyOption.REPLACE_EXISTING);
            } else {
                System.err.printf("Warning: Source file %s not found for %s, version %s%n", sourceFile, filename, version);
            }
        }
    }
    

    public class CurrentDate {
        public String currentDate() {
            LocalDate currentDate = LocalDate.now();
            return currentDate.toString();
        }
    } // public class CurrentDate

    public class FileHasher {
        private static final int HASH_LEN = 16;

        public String hashFile(String filename) {
            String hashCode = null;
            Path filePath = Path.of(filename);
            hashCode = calculateHash(filePath);
            return hashCode;
        } // public String hashFile(String filename)
        
        private String calculateHash(Path file) {
            try {
                byte[] data = Files.readAllBytes(file);  // Read entire file at once
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hashBytes = digest.digest(data);

                // Convert hashBytes to hex with desired truncation length
                return bytesToHex(hashBytes, HASH_LEN);

            } catch (IOException | NoSuchAlgorithmException e) {
                e.printStackTrace();
                return null;
            }
        } // private String calculateHash(Path file)

        private String bytesToHex(byte[] bytes, int length) {
            StringBuilder hexString = new StringBuilder();
            for (int i = 0; i < bytes.length && hexString.length() < length; i++) {
                String hex = Integer.toHexString(0xff & bytes[i]);
                if (hex.length() == 1)
                    hexString.append('0'); // Pad with leading zero if needed
                hexString.append(hex);
            }
            return hexString.substring(0, Math.min(length, hexString.length()));
        } // private String bytesToHex(byte[] bytes, int length)
    } // public class FileHasher

    public class FileCreator {
        private Path tigDir;
        public FileCreator() {
            this.tigDir = Paths.get(".tig");
        } // public FileCreator()
        public void createFile(String filename) {
            Path filePath = tigDir.resolve(filename);
            try {
                if (!Files.exists(filePath)) {
                    Files.createFile(filePath);
                    // System.out.println("DEBUG: File created: " + filename + "\n");
                } // if (!Files.exists(filePath))
            } catch (IOException e) {
                System.err.println("Error: " + e.getMessage() + "\n");
            } // try catch
        } // public void createFile(String filename)
    } // public class FileCreator

    public class StagedWriter {
        protected String hashCode = null;
        protected String filename = null;
        protected Path stagedPath = Paths.get(".tig/staged.json");
        public StagedWriter(String filename) {
            FileHasher fileHasher = new FileHasher();
            this.filename = filename;
            this.hashCode = fileHasher.hashFile(filename);
            
            try {
                updateStaged();
            } catch (IOException e) {
                System.err.println("Error: " + e.getMessage() + "\n");
            }
        } // public StagedWriter()
        
        public void updateStaged() throws IOException {
            // Ensure the staged.json exists
            if (!Files.exists(stagedPath)) {
                Files.createFile(stagedPath);
            }
            Map<String, String> jsonMap = new HashMap<>();
            File file = this.stagedPath.toFile();

            // if staged.json is not empty
            if (file.length() > 0) {
                try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                    StringBuilder jsonBuilder = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        jsonBuilder.append(line);
                    }
                    String jsonString = jsonBuilder.toString();
                    jsonMap = parseJson(jsonString);
                } 
            } // if (file.length() > 0)

            jsonMap.put(this.filename, this.hashCode);

            try (BufferedWriter writer = new BufferedWriter((new FileWriter(file)))) {
                String updatedJson = toJson(jsonMap);
                writer.write(updatedJson);
                // System.out.println("Updated JSON file: " + updatedJson);
            }
        } // public void updateStaged(Path filePath, String filename, String hashCode)

        public static Map<String, String> parseJson(String jsonString) {
            Map<String, String> map = new HashMap<>();
            if (jsonString.trim().isEmpty()) {
                return map;
            }

            jsonString = jsonString.trim();
            
            if (jsonString.length() > 2) {
                jsonString = jsonString.substring(1, jsonString.length() - 1); // Remove curly braces
            }

            String[] entries = jsonString.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"); // Split by commas outside quotes

            for (String entry : entries) {
                String[] keyValue = entry.split(":(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"); // Split by colon outside quotes
                if (keyValue.length == 2) {
                    String key = keyValue[0].trim().replaceAll("^\"|\"$", ""); // Remove surrounding quotes
                    String value = keyValue[1].trim().replaceAll("^\"|\"$", ""); // Remove surrounding quotes
                    map.put(key, value);
                }
            }

            return map;
        } // public static Map<String, String> parseJson(String jsonString)

        // Helper method to convert a Map into a JSON string
        public static String toJson(Map<String, String> map) {
            StringBuilder jsonBuilder = new StringBuilder();
            jsonBuilder.append("{");
            Iterator<Map.Entry<String, String>> iterator = map.entrySet().iterator();

            while (iterator.hasNext()) {
                Map.Entry<String, String> entry = iterator.next();
                jsonBuilder.append("\"").append(entry.getKey()).append("\": \"").append(entry.getValue()).append("\"");
                if (iterator.hasNext()) {
                    jsonBuilder.append(", ");
                }
            }

            jsonBuilder.append("}");
            return jsonBuilder.toString();
        } // public static String toJson(Map<String, String> map)
    } // public class StagedWriter

    public class CommitWriter {
        private final File commitLogFile;
        private final File stagedFile;
        private final File repoRoot;

        public CommitWriter() {
            this.commitLogFile = new File(".tig/commitLog.json");
            this.stagedFile = new File(".tig/staged.json");
            this.repoRoot = new File(".");
        }

        public void writeLog(String message) {
            List<Map<String, Object>> commitLog = new ArrayList<>();
            Map<String, Object> stagedManifest;
            Map<String, Object> previousLocationDictionary;
            // for fileLocation.json
            Map<String, Object> locationDictionary = new java.util.HashMap<>();
            int newCommitId = 1;
            int previousCommitId = 1;
            String previousCommitIdString = "1";
            
            try {
                // Read staged.json file
                stagedManifest = readJsonFile(stagedFile);
                if (stagedManifest.isEmpty()) {
                    System.out.println("No files staged for commit.");
                    return;
                }
                // If commitLog.json exists and is not empty
                if (commitLogFile.exists() && commitLogFile.length() > 0) {
                    commitLog = readJsonFileAsList(commitLogFile);
                    // System.out.println("DEBUG: CommitWriter: commitLog: '" + commitLog + "'\n");
                    if (!commitLog.isEmpty()) {
                        Map<String, Object> lastCommit = commitLog.get(commitLog.size() - 1);
                        
                        // Debugging output for manifest
                        Object manifestObject = lastCommit.get("manifest");
                        // System.out.println("DEBUG: Last commit manifest read as: " + manifestObject);
                        
                        // Retrieve and convert commitId safely
                        Object commitIdObj = lastCommit.get("commitId");
                        if (commitIdObj instanceof String) {
                            newCommitId = Integer.parseInt((String) commitIdObj) + 1;
                        } else if (commitIdObj instanceof Integer) {
                            newCommitId = (int) commitIdObj + 1;
                        }    
                        // Copy staged files to the new commit directory
                        copyStagedFiles(newCommitId, stagedManifest);
                        
                        // update the previous commitId for fileLocation.json
                        if (newCommitId != 1) {
                            previousCommitId = newCommitId - 1;
                            previousCommitIdString = String.valueOf(previousCommitId);
                            // update the path to the previous commit directory
                            // update fileLocation.json
                            File previousLocationFile = new File(".tig/" + previousCommitIdString + "/fileLocation.json");
                            previousLocationDictionary = readJsonFile(previousLocationFile);
                            locationDictionary = previousLocationDictionary;
                        }
                        for (String filename : stagedManifest.keySet()) {
                            locationDictionary.put(filename, String.valueOf(newCommitId));
                        }
                        File locationFile = new File(".tig/" + String.valueOf(newCommitId) + "/fileLocation.json");
                        
                        try (BufferedWriter writer = new BufferedWriter(new FileWriter(locationFile))) {
                                Map<String, Object> entry = locationDictionary;
                                writer.write("  {\n");
                                int entryCount = 0;
                                for (Map.Entry<String, Object> e : entry.entrySet()) {
                                    if (e.getValue() instanceof Map) {
                                        writer.write(String.format("    \"%s\": %s%s\n", e.getKey(),
                                                formatNestedMap((Map<?, ?>) e.getValue()),
                                                entryCount < entry.size() - 1 ? "," : ""));
                                    } else {
                                        writer.write(String.format("    \"%s\": \"%s\"%s\n", e.getKey(), e.getValue(),
                                                entryCount < entry.size() - 1 ? "," : ""));
                                    }
                                    entryCount++;
                                }
                                writer.write("  }\n");
                            
                        }

                        
                        // [stagedManifest Changed] Retrieve previous manifest and merge it with staged manifest
                        if (manifestObject instanceof Map) {
                            Map<String, Object> previousManifest = castToMap(manifestObject);
                            Map<String, Object> previousManifestCopy = deepCopy(previousManifest);
                            previousManifestCopy.putAll(stagedManifest); // Merge previous and new manifests
                            stagedManifest = previousManifestCopy;
                            // System.out.println("DEBUG: CommitWriter: stagedManifest:'" + stagedManifest + "'\n" );
                        }
                    }
                }
                
                // Create new commit entry
                Map<String, Object> newCommitEntry = new LinkedHashMap<>();
                CurrentDate date = new CurrentDate();
                newCommitEntry.put("commitId", String.valueOf(newCommitId)); // Keep commitId as String for JSON
                // consistency
                newCommitEntry.put("date", date.currentDate());
                newCommitEntry.put("message", message);
                newCommitEntry.put("manifest", stagedManifest); // Nested manifest
                
                if (!(commitLogFile.exists() && commitLogFile.length() > 0)){
                    // Copy staged files to the new commit directory
                    copyStagedFiles(newCommitId, stagedManifest);
                    for (String filename : stagedManifest.keySet()) {
                        locationDictionary.put(filename, String.valueOf(newCommitId));
                    }
                    File locationFile = new File(".tig/" + String.valueOf(newCommitId) + "/fileLocation.json");

                    try (BufferedWriter writer = new BufferedWriter(new FileWriter(locationFile))) {
                        Map<String, Object> entry = locationDictionary;
                        writer.write("  {\n");
                        int entryCount = 0;
                        for (Map.Entry<String, Object> e : entry.entrySet()) {
                            if (e.getValue() instanceof Map) {
                                writer.write(String.format("    \"%s\": %s%s\n", e.getKey(),
                                        formatNestedMap((Map<?, ?>) e.getValue()),
                                        entryCount < entry.size() - 1 ? "," : ""));
                            } else {
                                writer.write(String.format("    \"%s\": \"%s\"%s\n", e.getKey(), e.getValue(),
                                        entryCount < entry.size() - 1 ? "," : ""));
                            }
                            entryCount++;
                        }
                        writer.write("  }\n");

                    }
                }
                // Append new commit entry
                commitLog.add(newCommitEntry);
                
                // Write the updated log
                writeJsonToFile(commitLogFile, commitLog);
                

                // Clear staged.json
                clearFile(stagedFile);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        private void copyStagedFiles(int commitId, Map<String, Object> manifest) {
            File commitDir = new File(".tig/" + commitId);
            if (!commitDir.exists() && !commitDir.mkdirs()) {
                System.out.println("ERROR: Failed to create directory for commit " + commitId);
                return;
            }
            for (String fileName : manifest.keySet()) {
                File sourceFile = new File(repoRoot, fileName);
                File destFile = new File(commitDir, fileName);
                try {
                    // Ensure parent directories are created
                    if (destFile.getParentFile() != null) {
                        destFile.getParentFile().mkdirs();
                    }
                    Files.copy(sourceFile.toPath(), destFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
                    // System.out.println("Copied: " + sourceFile + " -> " + destFile);
                } catch (IOException e) {
                    System.out.println("ERROR: Failed to copy file " + fileName + " to commit directory.");
                    e.printStackTrace();
                }
            }
        }

        private Map<String, Object> readJsonFile(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new LinkedHashMap<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                return parseToMap(jsonContent.toString());
            }
        }

        private List<Map<String, Object>> readJsonFileAsList(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new ArrayList<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                // 'jsonContent.toString()' is the entire content of commitLog.json as a string
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                // System.out.println("DEBUG: readJsonFileAsList; jsonContent: '" + jsonContent.toString() + "'\n");
                return parseToList(jsonContent.toString());
            }
        }

        private Map<String, Object> parseToMap(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("{") && json.endsWith("}")) {
                Map<String, Object> map = new LinkedHashMap<>();
                String content = json.substring(1, json.length() - 1);

                // Use a more robust method to split key-value pairs
                int depth = 0;
                StringBuilder buffer = new StringBuilder();
                List<String> pairs = new ArrayList<>();

                for (char c : content.toCharArray()) {
                    if (c == ',' && depth == 0) {
                        pairs.add(buffer.toString().trim());
                        buffer.setLength(0);
                    } else {
                        buffer.append(c);
                        if (c == '{' || c == '[')
                            depth++;
                        if (c == '}' || c == ']')
                            depth--;
                    }
                }
                if (buffer.length() > 0) {
                    pairs.add(buffer.toString().trim());
                }

                // Parse key-value pairs
                for (String pair : pairs) {
                    String[] keyValue = pair.split(":", 2);
                    if (keyValue.length < 2) {
                        throw new IOException("Invalid JSON format: " + pair);
                    }
                    String key = keyValue[0].trim().replaceAll("^\"|\"$", "");
                    String value = keyValue[1].trim();

                    if (value.startsWith("{")) {
                        map.put(key, parseToMap(value));
                    } else if (value.startsWith("[")) {
                        map.put(key, parseToList(value));
                    } else {
                        map.put(key, value.replaceAll("^\"|\"$", ""));
                    }
                }
                return map;
            }
            return new LinkedHashMap<>();

        }

        private List<Map<String, Object>> parseToList(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("[") && json.endsWith("]")) {
                List<Map<String, Object>> list = new ArrayList<>();
                String content = json.substring(1, json.length() - 1);
                // content is jsonContent without []
                // System.out.println("DEBUG: parseToList: content: '" + content + "'\n");
                // The following is not doing anything.
                String[] objects = content.split("\\},\\s*(?=\\{)");
                // System.out.println("DEBUG: parseToList: objects[0]: '" + objects[0]+ "'\n");
                for (String obj : objects) {
                    if (!obj.endsWith("}"))
                        obj += "}";
                    // System.out.println("DEBUG: obj: '" + obj + "'\n");
                    list.add(parseToMap(obj));
                }
                return list;
            }
            return new ArrayList<>();
        }

        @SuppressWarnings("unchecked")
        private Map<String, Object> castToMap(Object object) {
            return (Map<String, Object>) object;
        }

        @SuppressWarnings("unchecked")
        public static Map<String, String> castToStringMap(Map<String, Object> map) {
            for (Object value : map.values()) {
                if (!(value instanceof String)) {
                    throw new IllegalArgumentException("Map contains non-String values: " + value);
                }
            }
            return (Map<String, String>) (Map<?, ?>) map;
        }

        private void writeJsonToFile(File file, List<Map<String, Object>> commitLog) throws IOException {
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
                writer.write("[\n");
                for (int i = 0; i < commitLog.size(); i++) {
                    Map<String, Object> entry = commitLog.get(i);
                    writer.write("  {\n");
                    int entryCount = 0;
                    for (Map.Entry<String, Object> e : entry.entrySet()) {
                        if (e.getValue() instanceof Map) {
                            writer.write(String.format("    \"%s\": %s%s\n", e.getKey(),
                                    formatNestedMap((Map<?, ?>) e.getValue()),
                                    entryCount < entry.size() - 1 ? "," : ""));
                        } else {
                            writer.write(String.format("    \"%s\": \"%s\"%s\n", e.getKey(), e.getValue(),
                                    entryCount < entry.size() - 1 ? "," : ""));
                        }
                        entryCount++;
                    }
                    writer.write("  }" + (i < commitLog.size() - 1 ? "," : "") + "\n");
                }
                writer.write("]");
            }
        }

        private String formatNestedMap(Map<?, ?> map) {
            StringBuilder result = new StringBuilder("{");
            int count = 0;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                result.append("\"").append(entry.getKey()).append("\": \"").append(entry.getValue()).append("\"");
                if (++count < map.size())
                    result.append(", ");
            }
            result.append("}");
            return result.toString();
        }

        public Map<String, Object> deepCopy(Map<String, Object> original) {
            Map<String, Object> copy = new HashMap<>();
            for (Map.Entry<String, Object> entry : original.entrySet()) {
                String key = entry.getKey();
                Object value = entry.getValue();

                // Perform a deep copy for nested objects
                if (value instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> nestedMap = (Map<String, Object>) value;
                    copy.put(key, deepCopy(nestedMap));
                } else if (value instanceof List) {
                    @SuppressWarnings("unchecked")
                    List<Object> list = (List<Object>) value;
                    copy.put(key, deepCopyList(list));
                } else {
                    // For primitive types and immutable objects, you can directly copy the value
                    copy.put(key, value);
                }
            }
            return copy;
        }

        private List<Object> deepCopyList(List<Object> original) {
            List<Object> copy = new ArrayList<>();
            for (Object item : original) {
                if (item instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> nestedMap = (Map<String, Object>) item;
                    copy.add(deepCopy(nestedMap));
                } else if (item instanceof List) {
                    @SuppressWarnings("unchecked")
                    List<Object> nestedList = (List<Object>) item;
                    copy.add(deepCopyList(nestedList));
                } else {
                    // For primitive types and immutable objects, directly copy the item
                    copy.add(item);
                }
            }
            return copy;
        }

        private void clearFile(File file) throws IOException {
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
                writer.write("");
            }
        }
    }

    public class Log {
        private final File commitLogFile;
        private final File stagedFile;
        private final File repoRoot;

        public Log() {
            this.commitLogFile = new File(".tig/commitLog.json");
            this.stagedFile = new File(".tig/staged.json");
            this.repoRoot = new File(".");
        }

        public void showLog(String number) {
            List<Map<String, Object>> commitLog = new ArrayList<>();
            Map<String, Object> stagedManifest;
            int commitId = 1;
            String commitDate = null;
            String commitMessage = null;
            int iteration = 5;

            try {
                // Remove negative sign and convert to integer
                iteration = Integer.parseInt(number.replace("-", ""));
                System.out.println("\nCommit Log\n----------\n");
                // System.out.println("DEBUG: showLog: iteration: '" + iteration + "'\n");

                // If commitLog.json exists and is not empty
                if (commitLogFile.exists() && commitLogFile.length() > 0) {
                    commitLog = readJsonFileAsList(commitLogFile);
                    // System.out.println("DEBUG: CommitWriter: commitLog: '" + commitLog + "'\n");
                    // System.out.println("DEBUG: showLog: commitLog length: '" + commitLog.size() + "'\n");
                    
                    if (iteration > commitLog.size()) {
                        iteration = commitLog.size();
                    }
                    // System.out.println("DEBUG: showLog: updated iteration: '" + iteration + "'\n");
                    
                    if (!commitLog.isEmpty()) {
                        for (int i = 0; i < iteration; i++) {
                            // System.out.println("DEBUG: showLog: i: '" + i + "'\n");
                            Map<String, Object> commit = commitLog.get(commitLog.size() - i - 1);
                            // commit id
                            Object commitIdObj = commit.get("commitId");
                            if (commitIdObj instanceof String) {
                                commitId = Integer.parseInt((String) commitIdObj);
                            } else if (commitIdObj instanceof Integer) {
                                commitId = (int) commitIdObj;
                            }
                            // commit date
                            Object commitDateObj = commit.get("date");
                            commitDate = (String) commitDateObj;
                            // commit message
                            Object commitMessageObj = commit.get("message");
                            commitMessage = (String) commitMessageObj;
                            System.out.println("commit ID: " + commitId + "\n");
                            System.out.println("commit Date: " + commitDate + "\n");
                            System.out.println("commit Message: '" + commitMessage + "'\n");
                            System.out.println("\n");

                        }
                        // Retrieve and convert commitId safely

                    } else {
                        System.out.println("Commit log is empty\n");
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        private Map<String, Object> readJsonFile(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new LinkedHashMap<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                return parseToMap(jsonContent.toString());
            }
        }

        private List<Map<String, Object>> readJsonFileAsList(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new ArrayList<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                // 'jsonContent.toString()' is the entire content of commitLog.json as a string
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                // System.out.println("DEBUG: readJsonFileAsList; jsonContent: '" +
                // jsonContent.toString() + "'\n");
                return parseToList(jsonContent.toString());
            }
        }

        private Map<String, Object> parseToMap(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("{") && json.endsWith("}")) {
                Map<String, Object> map = new LinkedHashMap<>();
                String content = json.substring(1, json.length() - 1);

                // Use a more robust method to split key-value pairs
                int depth = 0;
                StringBuilder buffer = new StringBuilder();
                List<String> pairs = new ArrayList<>();

                for (char c : content.toCharArray()) {
                    if (c == ',' && depth == 0) {
                        pairs.add(buffer.toString().trim());
                        buffer.setLength(0);
                    } else {
                        buffer.append(c);
                        if (c == '{' || c == '[')
                            depth++;
                        if (c == '}' || c == ']')
                            depth--;
                    }
                }
                if (buffer.length() > 0) {
                    pairs.add(buffer.toString().trim());
                }

                // Parse key-value pairs
                for (String pair : pairs) {
                    String[] keyValue = pair.split(":", 2);
                    if (keyValue.length < 2) {
                        throw new IOException("Invalid JSON format: " + pair);
                    }
                    String key = keyValue[0].trim().replaceAll("^\"|\"$", "");
                    String value = keyValue[1].trim();

                    if (value.startsWith("{")) {
                        map.put(key, parseToMap(value));
                    } else if (value.startsWith("[")) {
                        map.put(key, parseToList(value));
                    } else {
                        map.put(key, value.replaceAll("^\"|\"$", ""));
                    }
                }
                return map;
            }
            return new LinkedHashMap<>();

        }

        private List<Map<String, Object>> parseToList(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("[") && json.endsWith("]")) {
                List<Map<String, Object>> list = new ArrayList<>();
                String content = json.substring(1, json.length() - 1);
                // content is jsonContent without []
                // System.out.println("DEBUG: parseToList: content: '" + content + "'\n");
                // The following is not doing anything.
                String[] objects = content.split("\\},\\s*(?=\\{)");
                // System.out.println("DEBUG: parseToList: objects[0]: '" + objects[0]+ "'\n");
                for (String obj : objects) {
                    if (!obj.endsWith("}"))
                        obj += "}";
                    // System.out.println("DEBUG: obj: '" + obj + "'\n");
                    list.add(parseToMap(obj));
                }
                return list;
            }
            return new ArrayList<>();
        }

        @SuppressWarnings("unchecked")
        public static Map<String, String> castToStringMap(Map<String, Object> map) {
            for (Object value : map.values()) {
                if (!(value instanceof String)) {
                    throw new IllegalArgumentException("Map contains non-String values: " + value);
                }
            }
            return (Map<String, String>) (Map<?, ?>) map;
        }

        private String formatNestedMap(Map<?, ?> map) {
            StringBuilder result = new StringBuilder("{");
            int count = 0;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                result.append("\"").append(entry.getKey()).append("\": \"").append(entry.getValue()).append("\"");
                if (++count < map.size())
                    result.append(", ");
            }
            result.append("}");
            return result.toString();
        }

        public Map<String, Object> deepCopy(Map<String, Object> original) {
            Map<String, Object> copy = new HashMap<>();
            for (Map.Entry<String, Object> entry : original.entrySet()) {
                String key = entry.getKey();
                Object value = entry.getValue();

                // Perform a deep copy for nested objects
                if (value instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> nestedMap = (Map<String, Object>) value;
                    copy.put(key, deepCopy(nestedMap));
                } else if (value instanceof List) {
                    @SuppressWarnings("unchecked")
                    List<Object> list = (List<Object>) value;
                    copy.put(key, deepCopyList(list));
                } else {
                    // For primitive types and immutable objects, you can directly copy the value
                    copy.put(key, value);
                }
            }
            return copy;
        }

        private List<Object> deepCopyList(List<Object> original) {
            List<Object> copy = new ArrayList<>();
            for (Object item : original) {
                if (item instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> nestedMap = (Map<String, Object>) item;
                    copy.add(deepCopy(nestedMap));
                } else if (item instanceof List) {
                    @SuppressWarnings("unchecked")
                    List<Object> nestedList = (List<Object>) item;
                    copy.add(deepCopyList(nestedList));
                } else {
                    // For primitive types and immutable objects, directly copy the item
                    copy.add(item);
                }
            }
            return copy;
        }
    }

    public class Status {
        private final File repoRoot;
        private final File stagedFile;
        private final File commitLogFile;

        public Status() {
            this.repoRoot = new File(".");
            this.stagedFile = new File(".tig/staged.json");
            this.commitLogFile = new File(".tig/commitLog.json");
        }

        public void checkStatus() {
            File[] files = repoRoot.listFiles((dir, name) -> !name.equals(".tig"));
            Map<String, String> stagedManifest = null;
            List<Map<String, Object>> commitLog = null;
            if (files == null) {
                System.out.println("ERROR: Failed to list files in the repository.");
                return;
            }
            try {
                stagedManifest = castToStringMap(readJsonFile(stagedFile));
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }
            try {
                commitLog = readJsonFileAsList(commitLogFile);
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }

            Map<String, String> lastManifest = new LinkedHashMap<>();
            if (!commitLog.isEmpty()) {
                // System.out.println("DEBUG: status: commitLog: '" + commitLog + "'\n");
                Map<String, Object> lastCommit = commitLog.get(commitLog.size() - 1);
                // System.out.println("DEBUG: status: lastCommit: '" + lastCommit + "'\n");
                Object manifestObj = lastCommit.get("manifest");
                // System.out.println("DEBUG: status: manifestObj: '" + manifestObj + "'\n");
                if (manifestObj instanceof Map) {
                    lastManifest = castToStringMap(castToMap(manifestObj));
                }
            }

            FileHasher hasher = new FileHasher();

            for (File file : files) {
                String fileName = file.getName();
                if (stagedManifest.containsKey(fileName)) {
                    System.out.println(fileName + " -- staged");
                } else if (lastManifest.containsKey(fileName)) {
                    String currentHash = hasher.hashFile(fileName);
                    if (currentHash.equals(lastManifest.get(fileName))) {
                        System.out.println(fileName + " -- committed");
                    } else {
                        System.out.println(fileName + " -- modified");
                    }
                } else {
                    System.out.println(fileName + " -- untracked");
                }
            }
        }

        private Map<String, Object> readJsonFile(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new LinkedHashMap<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                return parseToMap(jsonContent.toString());
            }
        }

        private List<Map<String, Object>> readJsonFileAsList(File file) throws IOException {
            if (!file.exists() || file.length() == 0)
                return new ArrayList<>();
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                StringBuilder jsonContent = new StringBuilder();
                String line;
                // 'jsonContent.toString()' is the entire content of commitLog.json as a string
                while ((line = reader.readLine()) != null) {
                    jsonContent.append(line);
                }
                // System.out.println("DEBUG: readJsonFileAsList; jsonContent: '" + jsonContent.toString() + "'\n");
                return parseToList(jsonContent.toString());
            }
        }

        private Map<String, Object> parseToMap(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("{") && json.endsWith("}")) {
                Map<String, Object> map = new LinkedHashMap<>();
                String content = json.substring(1, json.length() - 1);
                
                // Use a more robust method to split key-value pairs
                int depth = 0;
                StringBuilder buffer = new StringBuilder();
                List<String> pairs = new ArrayList<>();
                
                for (char c : content.toCharArray()) {
                    if (c == ',' && depth == 0) {
                        pairs.add(buffer.toString().trim());
                        buffer.setLength(0);
                    } else {
                        buffer.append(c);
                        if (c == '{' || c == '[') depth++;
                        if (c == '}' || c == ']') depth--;
                    }
                }
                if (buffer.length() > 0) {
                    pairs.add(buffer.toString().trim());
                }
                
                // Parse key-value pairs
                for (String pair : pairs) {
                    String[] keyValue = pair.split(":", 2);
                    if (keyValue.length < 2) {
                        throw new IOException("Invalid JSON format: " + pair);
                    }
                    String key = keyValue[0].trim().replaceAll("^\"|\"$", "");
                    String value = keyValue[1].trim();
                    
                    if (value.startsWith("{")) {
                        map.put(key, parseToMap(value));
                    } else if (value.startsWith("[")) {
                        map.put(key, parseToList(value));
                    } else {
                        map.put(key, value.replaceAll("^\"|\"$", ""));
                    }
                }
                return map;
            }
            return new LinkedHashMap<>();

        }

        private List<Map<String, Object>> parseToList(String json) throws IOException {
            json = json.trim();
            if (json.startsWith("[") && json.endsWith("]")) {
                List<Map<String, Object>> list = new ArrayList<>();
                String content = json.substring(1, json.length() - 1);
                // content is jsonContent without []
                // System.out.println("DEBUG: parseToList: content: '" + content + "'\n");
                // The following is not doing anything.
                String[] objects = content.split("\\},\\s*(?=\\{)");
                // System.out.println("DEBUG: parseToList: objects[0]: '" + objects[0]+ "'\n");
                for (String obj : objects) {
                    if (!obj.endsWith("}"))
                        obj += "}";
                    // System.out.println("DEBUG: obj: '" + obj + "'\n");
                    list.add(parseToMap(obj));
                }
                return list;
            }
            return new ArrayList<>();
        }

        @SuppressWarnings("unchecked")
        private Map<String, Object> castToMap(Object object) {
            return (Map<String, Object>) object;
        }
        
        @SuppressWarnings("unchecked")
        public static Map<String, String> castToStringMap(Map<String, Object> map) {
            for (Object value : map.values()) {
                if (!(value instanceof String)) {
                    throw new IllegalArgumentException("Map contains non-String values: " + value);
                }
            }
            return (Map<String, String>) (Map<?, ?>) map;
        }
    }

    public class DiffStuff {

        public static int findHighestCommitId() throws IOException {
            // System.out.println("DEBUG: Using the findHighestCommitId command: ");
            try (DirectoryStream<Path> stream = Files.newDirectoryStream(Paths.get(".tig"), 
                    path -> Files.isDirectory(path) && path.getFileName().toString().matches("\\d+"))) {
                
                return StreamSupport.stream(stream.spliterator(), false)
                    .mapToInt(path -> Integer.parseInt(path.getFileName().toString()))
                    .max()
                    .orElseThrow(() -> new IOException("No commit directories found"));

                    
            }
        } // end of findHighestCommitId

        public static String createUnifiedDiff(Path oldFile, Path newFile) throws IOException {
            // Read lines from both files
            List<String> oldLines = Files.readAllLines(oldFile);
            List<String> newLines = Files.readAllLines(newFile);
            
            // Generate the patch
            Patch<String> patch = DiffUtils.diff(oldLines, newLines);
            
            // If no changes, return an empty string
            if (patch.getDeltas().isEmpty()) {
                System.out.println("--- " + oldFile);
                System.out.println("+++ " + newFile);
                return "";
            }
            
            
            // Create a StringBuilder to build the unified diff output
            StringBuilder diffOutput = new StringBuilder();
            
            // Add unified diff header
            diffOutput.append("--- ").append(oldFile.toString()).append("\n");
            diffOutput.append("+++ ").append(newFile.toString()).append("\n");
            
            // Process each delta (change) in the patch
            for (AbstractDelta<String> delta : patch.getDeltas()) {
                // Add context and change information
                diffOutput.append("@@ -")
                    .append(delta.getSource().getPosition() + 1)
                    .append(",")
                    .append(delta.getSource().getLines().size())  // Use size() instead of getSize()
                    .append(" +")
                    .append(delta.getTarget().getPosition() + 1)
                    .append(",")
                    .append(delta.getTarget().getLines().size())  // Use size() instead of getSize()
                    .append(" @@\n");
                
                // Handle different types of changes
                switch (delta.getType()) {
                    case DELETE:
                        // Deleted lines are prefixed with '-'
                        delta.getSource().getLines().forEach(line ->
                            diffOutput.append("-").append(line).append("\n"));
                        break;
                    case INSERT:
                        // Inserted lines are prefixed with '+'
                        delta.getTarget().getLines().forEach(line ->
                            diffOutput.append("+").append(line).append("\n"));
                        break;
                    case CHANGE:
                        // Deleted lines first (prefixed with '-')
                        delta.getSource().getLines().forEach(line ->
                            diffOutput.append("-").append(line).append("\n"));
                        // Then added lines (prefixed with '+')
                        delta.getTarget().getLines().forEach(line ->
                            diffOutput.append("+").append(line).append("\n"));
                        break;
                }
            }
            return diffOutput.toString();
        } //end createUnifiedDiff method
    } // end diffStuff class



    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.out.println("Usage: \n" + //
                    "javac -cp \"../lib/java-diff-utils-4.9.jar:.\" ../Tig.java \n" + //
                    "java -cp ../:../lib/java-diff-utils-4.9.jar Tig <method> <filename>\n");
            return;
        } // if (args.length < 1)
        String command = args[0];
        String argument = null;
        // System.out.println("DEBUG: command is '" + command + "' \n");
        if ((!command.equals("status")) && (!command.equals("log"))) {
            if (args.length < 2) {
                System.out.println("Error: command '" + command + "' requires an argument. \n");
                return;
            } // if (args.length < 2)
            argument = args[1];
            // System.out.println("DEBUG: argument is '" + argument + "' \n");
        } // if (command != "status" and command != "log")

        if ((command.equals("log")) && (args.length == 2)) {
            argument = args[1];
        }

        Tig tig = new Tig();
        
        switch (command) {
            case "init":
                // System.out.println("DEBUG: The command is 'init'.\n");
                tig.init(argument);
                break;
            case "add":
                // System.out.println("DEBUG: The command is 'add'.\n");
                tig.add(argument);
                break;
            case "commit":
                // System.out.println("DEBUG: The command is 'commit'.\n");
                tig.commit(argument);
                break;
            case "log":
                // System.out.println("DEBUG: The command is 'log'.\n");
                if (argument != null) {
                    // System.out.println("DEBUG: argument is not null\n");
                    if (!argument.matches("-\\d+")) {
                        System.err.println("Error: Invalid format for '-N'.\n");
                        return;
                    }
                    tig.log(argument);
                } else {
                    // System.out.println("DEBUG: argument is null\n");
                    tig.log("-5");
                }
                break;
            case "diff":
                // System.out.println("DEBUG: The command is 'diff' and the argument is: " + argument);
                tig.diff(argument);
                break;
            case "status":
                // System.out.println("DEBUG: The command is 'status'.\n");
                tig.status();
                break;
            case "checkout":
                // System.out.println("DEBUG: The command is 'checkout'.\n");
                tig.checkout(argument);
                break;
            default:
                System.out.println("Error: Unknown command '" + command + "'.\n");
        } // switch (command)
    } // public static void main(String[] args)

} // public class Tig
