import java.io.*;
import java.nio.file.*;
import java.time.Instant;
import java.util.List;

class ArchiveLocal extends Archive {
    private Path backupDir;

    public ArchiveLocal(String sourceDir, String backupDir) {
        super(sourceDir);
        this.backupDir = Paths.get(backupDir);
    }

    @Override
    protected void copyFiles(List<FileEntry> manifest) {
        for (FileEntry entry : manifest) {
            Path sourcePath = sourceDir.resolve(entry.filename());
            Path backupPath = backupDir.resolve(entry.hash() + ".bck");
            if (!Files.exists(backupPath)) {
                try {
                    Files.copy(sourcePath, backupPath);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    @Override
    protected void writeManifest(List<FileEntry> manifest) {
        String timestamp = getTimestamp();
        if (!Files.exists(backupDir)) {
            try {
                Files.createDirectories(backupDir);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        Path manifestFile = backupDir.resolve(timestamp + ".csv");
        try (FileWriter writer = new FileWriter(manifestFile.toFile())) {
            writer.write("filename,hash\n");
            for (FileEntry entry : manifest) {
                writer.write(entry.filename() + "," + entry.hash() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String getTimestamp() {
        return String.valueOf(Instant.now().getEpochSecond());
    }
}