<<<<<<< HEAD
# HdiffXezenov
=======
# 🛠️ HhdiffXezenov Patcher v6.3

[English](#english) | [ภาษาไทย](#ภาษาไทย)

---

## English

### 📝 Description
**HhdiffXezenov** is a smart, safe, and automated patching tool designed specifically for HoYoverse games (Star Rail, Zenless Zone Zero, Genshin Impact) and any projects using the HDiff system. It simplifies the manual patching process while ensuring maximum data safety.

### ✨ Key Features
*   **Multi-Game Support:** Automatically detects patching logic for Star Rail (JSON) and ZZZ (TXT/PKG).
*   **Atomic Backup:** Automatically creates a backup of original files before modifying or deleting them.
*   **Integrity Verification:** Double-checks MD5 hashes for both source files (before patch) and target files (after patch).
*   **Smart Extraction:** Automatically finds 7-Zip or WinRAR to extract patch archives (.7z, .zip, .rar).
*   **Progress Tracking:** Displays real-time progress percentage (%) and a detailed summary report.
*   **One-Click Restore:** Includes a built-in system to restore your game files from backups instantly.

### 📋 Requirements & Dependencies
*   **Python 3.6+**: No external pip packages required (uses Standard Library).
*   **7-Zip or WinRAR**: Required for automatic extraction of compressed patches.
*   **hpatchz.exe**: The core patching engine (must be in the same folder).
*   **Disk Space**: At least 2x the size of the patch for Backup and Temp files.

### 📥 Download Links
*   **Python:** [Official Site](https://www.python.org/downloads/)
*   **7-Zip:** [Official Site](https://www.7-zip.org/)
*   **HDiffPatch (hpatchz.exe):** [GitHub Releases](https://github.com/sisong/HDiffPatch/releases)

### 🚀 How to Use
1.  Place `HhdiffXezenov.py`, `run_patcher.bat`, and `hpatchz.exe` in the same folder.
2.  Run `run_patcher.bat`.
3.  Paste the path to your **Game Folder**.
4.  Paste the path to your **Patch Folder** (or the compressed .7z/.zip file).
5.  Wait for the process to complete and check the `Summary Report`.

### ⚠️ Disclaimer
This tool is provided "as is", without warranty of any kind. The developers are not responsible for any data loss or game file corruption. Use it at your own risk.

---

## ภาษาไทย

### 📝 คำอธิบาย
**HhdiffXezenov** คือเครื่องมือ Patch เกมที่เน้นความฉลาดและปลอดภัย พัฒนามาเพื่อเกมค่าย HoYoverse (Star Rail, ZZZ, Genshin) และโปรเจกต์ที่ใช้ระบบ HDiff โดยเฉพาะ ช่วยลดความยุ่งยากในการอัปเดตเกมด้วยตัวเองพร้อมระบบป้องกันข้อมูลเสียหายสูงสุด

### ✨ ฟีเจอร์หลัก
*   **รองรับหลายเกม:** ตรวจสอบระบบการ Patch ของ Star Rail (JSON) และ ZZZ (TXT/PKG) ได้โดยอัตโนมัติ
*   **ระบบสำรองข้อมูล:** สร้าง Backup ไฟล์ต้นฉบับให้อัตโนมัติก่อนที่จะมีการแก้ไขหรือลบไฟล์ใดๆ
*   **ตรวจสอบความถูกต้อง:** เช็คค่า MD5 ทั้งไฟล์ก่อนเริ่ม (Source) และหลังจบ (Target) เพื่อความแม่นยำ 100%
*   **แตกไฟล์อัตโนมัติ:** ค้นหา 7-Zip หรือ WinRAR ในเครื่องเพื่อแตกไฟล์ Patch (.7z, .zip, .rar) ให้เอง
*   **ติดตามสถานะ:** แสดงเปอร์เซ็นต์ความคืบหน้า (%) และสรุปผลการทำงานอย่างละเอียดท้ายงาน
*   **กู้คืนไฟล์ง่ายๆ:** มีระบบ Restore ในตัวเพื่อย้อนกลับไปใช้ไฟล์เดิมจาก Backup ได้ทันที

### 📋 สิ่งที่ต้องมี (Requirements)
*   **Python 3.6+**: ไม่ต้องติดตั้ง Package เสริม (ใช้เพียง Library มาตรฐาน)
*   **7-Zip หรือ WinRAR**: จำเป็นต้องมีเพื่อใช้แตกไฟล์ Patch อัตโนมัติ
*   **hpatchz.exe**: ตัวเครื่องยนต์หลักในการ Patch (ต้องวางไว้ในโฟลเดอร์เดียวกัน)
*   **พื้นที่ว่างในดิสก์**: ควรมีพื้นที่ว่างอย่างน้อย 2 เท่าของขนาด Patch สำหรับ Backup และไฟล์ชั่วคราว

### 📥 ลิงก์ดาวน์โหลด (Download Links)
*   **Python:** [ดาวน์โหลดที่นี่](https://www.python.org/downloads/)
*   **7-Zip:** [ดาวน์โหลดที่นี่](https://www.7-zip.org/)
*   **HDiffPatch (hpatchz.exe):** [ดาวน์โหลดที่นี่ (GitHub)](https://github.com/sisong/HDiffPatch/releases)

### 🚀 วิธีใช้งาน
1.  วางไฟล์ `HhdiffXezenov.py`, `run_patcher.bat` และ `hpatchz.exe` ไว้ในโฟลเดอร์เดียวกัน
2.  รันไฟล์ `run_patcher.bat`
3.  วางที่อยู่ (Path) ของ **โฟลเดอร์เกม**
4.  วางที่อยู่ (Path) ของ **โฟลเดอร์ Patch** (หรือไฟล์บีบอัด .7z/.zip)
5.  รอจนเสร็จสิ้นและตรวจสอบหน้าจอ `Summary Report`

### ⚠️ คำเตือน
เครื่องมือนี้จัดทำขึ้น "ตามสภาพ" โดยไม่มีการรับประกันใดๆ ผู้พัฒนาจะไม่รับผิดชอบต่อความเสียหายของข้อมูลหรือไฟล์เกมที่อาจเกิดขึ้น โปรดใช้งานด้วยความระมัดระวัง
>>>>>>> bb3b945 (Initial commit v6.3: Public Release Edition)
