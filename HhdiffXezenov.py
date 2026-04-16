import os
import json
import subprocess
import hashlib
import shutil
import tempfile
import sys
from datetime import datetime

# ========================================================================
# 🛠️ HhdiffXezenov Patcher v6.3 (Public Release Edition)
# 📜 License: MIT
# ⚠️ Disclaimer: This tool is provided "as is", without warranty of any kind.
# ========================================================================

class Logger:
    """
    Custom logger to write output to both console and a fresh @log.txt file.
    ระบบบันทึก Log ที่แสดงผลทั้งบนหน้าจอและบันทึกลงไฟล์ @log.txt แบบล้างใหม่ทุกครั้ง
    """
    def __init__(self, filename="@log.txt"):
        self.terminal = sys.stdout
        # "w" mode clears old logs on every run | โหมด "w" จะลบ log เก่าทิ้งทุกครั้งที่เริ่มโปรแกรม
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Redirect stdout and stderr to our logger | เปลี่ยนทิศทาง Output ทั้งหมดไปยัง Logger ของเรา
sys.stdout = Logger()
sys.stderr = sys.stdout

def get_file_md5(file_path):
    """
    Calculate MD5 hash of a file for integrity verification.
    คำนวณค่า MD5 ของไฟล์เพื่อใช้ตรวจสอบความถูกต้องของข้อมูล
    """
    if not os.path.exists(file_path): return None
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024*1024), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def find_extractor():
    """
    Automatically search for 7-Zip or WinRAR in the system.
    ค้นหาโปรแกรม 7-Zip หรือ WinRAR ในเครื่องโดยอัตโนมัติ
    """
    standard_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
        r"C:\Program Files\WinRAR\WinRAR.exe",
    ]
    # Check Environment PATH | ตรวจสอบจาก PATH ของระบบ
    for cmd in ["7z", "7za", "rar"]:
        if shutil.which(cmd):
            return cmd
    # Check standard installation paths | ตรวจสอบจากโฟลเดอร์ติดตั้งมาตรฐาน
    for path in standard_paths:
        if os.path.exists(path):
            return f'"{path}"'
    return None

def extract_archive(archive_path, temp_root):
    """
    Extract compressed patch files to a temporary folder.
    แตกไฟล์ Patch ที่บีบอัดอยู่ไปยังโฟลเดอร์ชั่วคราว
    """
    print(f"\n📦 [1/5] Extracting archive... | ขั้นตอนการแตกไฟล์บีบอัด")
    print(f"   > File: {os.path.basename(archive_path)}")
    temp_dir = tempfile.mkdtemp(dir=temp_root)
    
    # Try internal shutil first | ลองใช้ระบบภายในของ Python ก่อน
    try:
        shutil.unpack_archive(archive_path, temp_dir)
        print(f"   ✅ Extraction successful (Internal Method)")
        return temp_dir
    except: pass

    # Try external extractors (7-Zip/WinRAR) | ลองใช้โปรแกรมภายนอก (7-Zip/WinRAR)
    extractor = find_extractor()
    if extractor:
        try:
            if "7z" in extractor.lower():
                subprocess.run(f'{extractor} x "{archive_path}" -o"{temp_dir}" -y', shell=True, check=True, capture_output=True)
            elif "rar" in extractor.lower():
                subprocess.run(f'{extractor} x "{archive_path}" "{temp_dir}\\" -y', shell=True, check=True, capture_output=True)
            print(f"   ✅ Extraction successful ({extractor})")
            return temp_dir
        except Exception as e:
            print(f"   ❌ Extraction failed: {str(e)}")
    
    print(f"   ❌ No extractor found! Please extract manually. | ไม่พบโปรแกรมแตกไฟล์! กรุณาแตกไฟล์เอง")
    return None

def start_patching():
    """
    Main patching process logic. | ตรรกะหลักของกระบวนการ Patch ทั้งหมด
    """
    print(f"\n🚀 --- HhdiffXezenov Patcher v6.3 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print("⚠️  Warning: Ensure you have enough disk space for backups and new files.")
    print("⚠️  คำเตือน: โปรดตรวจสอบว่ามีพื้นที่ว่างเพียงพอสำหรับการ Backup และไฟล์ใหม่\n")
    
    game_dir = input("📂 Game Folder Path (วาง Path เกม): ").strip('"').strip()
    patch_input = input("📦 Patch Path/File (วาง Path หรือไฟล์ Patch): ").strip('"').strip()
    
    if not os.path.exists(game_dir):
        print("❌ Game folder not found! | ไม่พบโฟลเดอร์เกม!")
        return

    # Prepare Temp and Backup paths | เตรียมโฟลเดอร์ชั่วคราวและที่เก็บ Backup
    temp_root = os.path.join(game_dir, "_HDiff_Temp")
    os.makedirs(temp_root, exist_ok=True)
    
    is_temp_patch = False
    patch_dir = patch_input
    if os.path.isfile(patch_input):
        patch_dir = extract_archive(patch_input, temp_root)
        if not patch_dir: return
        is_temp_patch = True

    # Search for hpatchz.exe | ค้นหาตัวรัน hpatchz.exe
    hpatchz = "hpatchz.exe"
    if not os.path.exists(hpatchz):
        hpatchz = os.path.join(os.getcwd(), "hpatchz.exe")
        if not os.path.exists(hpatchz):
            alt_hpatchz = os.path.join(patch_dir, "hpatchz.exe")
            if os.path.exists(alt_hpatchz):
                hpatchz = alt_hpatchz
            else:
                print("❌ hpatchz.exe not found! | ไม่พบ hpatchz.exe!")
                return

    # Create backup point | สร้างจุดสำรองข้อมูล
    backup_base = os.path.join(game_dir, f"_HDiff_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_base, exist_ok=True)
    print(f"\n🛡️  [2/5] Created backup point: {os.path.basename(backup_base)}")

    # Statistics for summary | เก็บสถิติเพื่อสรุปผล
    stats = {"success": 0, "fail": 0, "skip": 0, "details": []}

    try:
        # Analyze Patch Structure | วิเคราะห์โครงสร้าง Patch
        patch_list = []
        pkg_map = {}
        pkg_path = os.path.join(patch_dir, "pkg_version")
        if os.path.exists(pkg_path):
            with open(pkg_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        pkg_map[data["remoteName"]] = data["md5"]
                    except: continue

        map_path = os.path.join(patch_dir, "hdiffmap.json")
        zzz_map_path = os.path.join(patch_dir, "hdifffiles.txt")

        if os.path.exists(map_path):
            print("🔍 [3/5] Mode: Star Rail / Genshin Impact")
            with open(map_path, 'r', encoding='utf-8') as f:
                data = json.load(f).get("diff_map", [])
                for entry in data:
                    patch_list.append({
                        "source": entry["source_file_name"], 
                        "target": entry["target_file_name"], 
                        "patch": entry["patch_file_name"], 
                        "source_md5": entry["source_file_md5"], 
                        "target_md5": entry["target_file_md5"]
                    })
        elif os.path.exists(zzz_map_path):
            print("🔍 [3/5] Mode: ZZZ (Zenless Zone Zero)")
            with open(zzz_map_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        name = json.loads(line.strip())["remoteName"]
                        patch_list.append({
                            "source": name, "target": name, 
                            "patch": name + ".hdiff", 
                            "source_md5": None, "target_md5": pkg_map.get(name)
                        })
                    except: continue
        else:
            print("🔍 [3/5] Mode: Generic (Scan .hdiff files)")
            for root, dirs, files in os.walk(patch_dir):
                for f in files:
                    if f.endswith(".hdiff"):
                        rel_p = os.path.relpath(os.path.join(root, f), patch_dir)
                        rel_t = rel_p[:-6]
                        patch_list.append({
                            "source": rel_t, "target": rel_t, "patch": rel_p, 
                            "source_md5": None, "target_md5": pkg_map.get(rel_t)
                        })

        total = len(patch_list)
        if total == 0:
            print("⚠️ No patching tasks found! | ไม่พบรายการที่จะต้อง Patch!")
            return

        # Start Patching | เริ่มขั้นตอนการ Patch
        print(f"\n⚡ [4/5] Patching progress... ({total} files) | เริ่มขั้นตอนการ Patch")
        for i, entry in enumerate(patch_list, 1):
            percent = (i / total) * 100
            s_path = os.path.join(game_dir, entry["source"])
            p_path = os.path.join(patch_dir, entry["patch"])
            t_path = os.path.join(game_dir, entry["target"])
            
            if not os.path.exists(p_path):
                stats["skip"] += 1
                continue

            # Integrity Verification (Source) | ตรวจสอบไฟล์ต้นฉบับ
            if entry["source_md5"] and os.path.exists(s_path):
                if get_file_md5(s_path) != entry["source_md5"]:
                    print(f"   [{i}/{total}] {percent:5.1f}% ⚠️ Skipped: Source MD5 mismatch -> {entry['target']}")
                    stats["skip"] += 1
                    stats["details"].append(f"Skipped (MD5 mismatch): {entry['target']}")
                    continue

            print(f"   [{i}/{total}] {percent:5.1f}% Patching: {entry['target']}...", end="\r")
            os.makedirs(os.path.dirname(t_path), exist_ok=True)
            temp_file = t_path + ".tmp"
            
            # Execute hpatchz | สั่งรัน hpatchz
            cmd = [hpatchz, "-f", s_path if os.path.exists(s_path) else "", p_path, temp_file]
            if subprocess.run(cmd, capture_output=True).returncode == 0:
                # Integrity Verification (Target) | ตรวจสอบไฟล์ผลลัพธ์
                if not entry["target_md5"] or get_file_md5(temp_file) == entry["target_md5"]:
                    if os.path.exists(t_path):
                        # Move original to backup | ย้ายไฟล์เดิมไปที่ Backup
                        b_path = os.path.join(backup_base, entry["target"])
                        os.makedirs(os.path.dirname(b_path), exist_ok=True)
                        shutil.move(t_path, b_path)
                    os.rename(temp_file, t_path)
                    print(f"   [{i}/{total}] {percent:5.1f}% ✅ Success: {entry['target']}               ")
                    stats["success"] += 1
                else:
                    print(f"   [{i}/{total}] {percent:5.1f}% ❌ Failed: Target MD5 error -> {entry['target']}")
                    stats["fail"] += 1
                    stats["details"].append(f"Failed (Target MD5 mismatch): {entry['target']}")
                    if os.path.exists(temp_file): os.remove(temp_file)
            else:
                print(f"   [{i}/{total}] {percent:5.1f}% ❌ Failed: hpatchz execution error -> {entry['target']}")
                stats["fail"] += 1
                stats["details"].append(f"Failed (hpatchz error): {entry['target']}")

        # Resource Management (Delete/Copy) | จัดการไฟล์ทรัพยากร (ลบ/คัดลอก)
        print(f"\n📦 [5/5] Finalizing resource files... | ขั้นตอนสุดท้าย: จัดการไฟล์ทรัพยากร")
        
        # Process deletefiles.txt | จัดการไฟล์ที่ต้องลบ
        del_path = os.path.join(patch_dir, "deletefiles.txt")
        if os.path.exists(del_path):
            with open(del_path, 'r', encoding='utf-8') as f:
                for line in f:
                    f_rel = line.strip()
                    if f_rel and os.path.exists(os.path.join(game_dir, f_rel)):
                        dst = os.path.join(backup_base, f_rel)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.move(os.path.join(game_dir, f_rel), dst)

        # Copy non-patch files | คัดลอกไฟล์ใหม่ที่ไม่ได้มาจากการ Patch
        exclude = ["hdiffmap.json", "hdifffiles.txt", "deletefiles.txt", "hpatchz.exe", "pkg_version", "HhdiffXezenov.py", "run_patcher.bat", "@log.txt"]
        for root, dirs, files in os.walk(patch_dir):
            for file in files:
                if file.endswith(".hdiff") or file in exclude: continue
                src = os.path.join(root, file)
                rel = os.path.relpath(src, patch_dir)
                dst = os.path.join(game_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    b_dst = os.path.join(backup_base, rel)
                    os.makedirs(os.path.dirname(b_dst), exist_ok=True)
                    if not os.path.exists(b_dst): shutil.copy2(dst, b_dst)
                shutil.copy2(src, dst)
                print(f"   ✅ Updated resource: {rel}", end="\r")

    except Exception as e:
        print(f"\n❌ Critical Error: {str(e)}")
    finally:
        # Cleanup temp folder | ทำความสะอาดไฟล์ชั่วคราว
        if is_temp_patch: shutil.rmtree(patch_dir)
        if os.path.exists(temp_root) and not os.listdir(temp_root): os.rmdir(temp_root)

    # Summary Report | ตารางสรุปผล
    print("\n\n" + "="*60)
    print("📊 Verification Summary | สรุปผลการตรวจสอบ")
    print("="*60)
    print(f"✅ Patch Success (สำเร็จ):   {stats['success']} files")
    print(f"❌ Patch Failed (ล้มเหลว):    {stats['fail']} files")
    print(f"⚠️  Skipped/Error (ถูกข้าม):   {stats['skip']} files")
    print("-" * 60)
    if stats["fail"] > 0 or stats["skip"] > 0:
        print("🔍 Issue Details | รายละเอียดปัญหา:")
        for detail in stats["details"][:10]: print(f"   > {detail}")
        if len(stats["details"]) > 10: print(f"   ... and {len(stats['details'])-10} more.")
    else:
        print("✨ All files updated and verified successfully! 100%")
    print("="*60)

if __name__ == "__main__":
    # Clear console safely | ล้างหน้าจออย่างปลอดภัย
    if os.name == 'nt': subprocess.run("cls", shell=True)
    else: subprocess.run("clear", shell=True)

    print("╔══════════════════════════════════════════════════════╗")
    print("║          HhdiffXezenov Multi-Game Patcher            ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("1. Start Patching (เริ่มขั้นตอนอัปเดต)")
    print("2. Restore Backup (กู้คืนไฟล์จากจุดสำรองข้อมูลล่าสุด)")
    
    choice = input("\nSelect Mode (เลือกโหมด 1/2): ")
    if choice == "1":
        start_patching()
    elif choice == "2":
        print("⚠️ Feature coming soon or use previous stable version.")
    
    input("\nPress Enter to exit... | กด Enter เพื่อจบการทำงาน...")
