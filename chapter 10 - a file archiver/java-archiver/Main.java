public class Main {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Main source_dir backup_dir");
            System.exit(1);
        }
        String sourceDir = args[0];
        String backupDir = args[1];
        Archive archiver = new ArchiveLocal(sourceDir, backupDir);
        archiver.backup();
    }

}