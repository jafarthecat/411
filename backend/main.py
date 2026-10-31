import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import engine, init_db
from models import (
    Artifact, ArtifactDB, Faction, FactionDB, Persona, PersonaDB,
    QuizAnswers, ScanRequest, User, UserCollection, UserCollectionDB,
    UserDB, CollectionItemResponse
)

# ==========================================
# ฟังก์ชันสร้างข้อมูลตัวอย่าง (Seed Data)
# ==========================================
def seed_db():
    with Session(engine) as session:
        # เช็คว่ามี Faction ในระบบหรือยัง ถ้ายังไม่มีให้สร้างใหม่
        if not session.exec(select(FactionDB)).first():
            # 1. สร้าง Factions ครอบคลุมทุกโซน
            egypt = FactionDB(name="Egypt", total_rooms=4, description="อารยธรรมลุ่มแม่น้ำไนล์")
            greece = FactionDB(name="Greece", total_rooms=4, description="ดินแดนแห่งเทพเจ้าและนักปราชญ์")
            rome = FactionDB(name="Rome", total_rooms=4, description="จักรวรรดิโรมันอันยิ่งใหญ่")
            asia = FactionDB(name="Asia", total_rooms=10, description="ศิลปะและโบราณวัตถุแห่งเอเชีย")
            europe = FactionDB(name="Europe", total_rooms=10, description="ประวัติศาสตร์และอารยธรรมยุโรป")
            middle_east = FactionDB(name="Middle East", total_rooms=10, description="ดินแดนตะวันออกกลางและอาระเบีย")
            americas = FactionDB(name="Americas", total_rooms=5, description="อารยธรรมแห่งทวีปอเมริกา")
            africa = FactionDB(name="Africa", total_rooms=5, description="ศิลปะและอารยธรรมแห่งทวีปแอฟริกา")
            
            session.add_all([egypt, greece, rome, asia, europe, middle_east, americas, africa])
            session.commit()
            
            # 2. สร้าง Artifacts ทั้ง 16 ชิ้น
            artifacts = [
                ArtifactDB(
                    name="Colossal granite image of King Ramesses ll", 
                    room_no="4", 
                    gallery_name="Egyptian sculpture", 
                    qr_code_val="QR-1", 
                    clue_text="Colossal granite image of King Ramesses ll", 
                    silhouette_url="",
                    image_url="/images/artifact/Colossal granite image of King Ramesses ll.webp",
                    faction_id=egypt.id
                ),
                ArtifactDB(
                    name="Brass head of an Ooni", 
                    room_no="25", 
                    gallery_name="Africa", 
                    qr_code_val="QR-2", 
                    clue_text="Brass head of an Ooni", 
                    silhouette_url="",
                    image_url="/images/artifact/Brass head of an Ooni.webp",
                    faction_id=africa.id
                ),
                ArtifactDB(
                    name="The Sutton hoo helmet", 
                    room_no="41", 
                    gallery_name="Sutton Hoo and Europe", 
                    qr_code_val="QR-3", 
                    clue_text="The Sutton hoo helmet", 
                    silhouette_url="",
                    image_url="/images/artifact/The Sutton hoo helmet.webp",
                    faction_id=europe.id
                ),
                ArtifactDB(
                    name="The Portland Vase", 
                    room_no="70", 
                    gallery_name="Roman Empire", 
                    qr_code_val="QR-4", 
                    clue_text="The Portland Vase", 
                    silhouette_url="",
                    image_url="/images/artifact/The Portland Vase.webp",
                    faction_id=rome.id
                ),
                ArtifactDB(
                    name="Bust of Sir Hans Sloane", 
                    room_no="1", 
                    gallery_name="Enlightenment", 
                    qr_code_val="QR-5", 
                    clue_text="Bust of Sir Hans Sloane", 
                    silhouette_url="",
                    image_url="/images/artifact/Bust os Sir Hans Sloane.webp",
                    faction_id=europe.id
                ),
                ArtifactDB(
                    name="Relief panel from the Harpy Tomb", 
                    room_no="15", 
                    gallery_name="Greece: Athens and Lycia", 
                    qr_code_val="QR-6", 
                    clue_text="Relief panel from the Harpy Tomb", 
                    silhouette_url="",
                    image_url="/images/artifact/Relief panel from the Harpy Tomb.jpg",
                    faction_id=greece.id
                ),
                ArtifactDB(
                    name="Double-headed serpent mosaic", 
                    room_no="27", 
                    gallery_name="Mexico", 
                    qr_code_val="QR-7", 
                    clue_text="Double-headed serpent mosaic", 
                    silhouette_url="",
                    image_url="/images/artifact/Double-headed serpent mosaic.webp",
                    faction_id=americas.id
                ),
                ArtifactDB(
                    name="The goddess tara", 
                    room_no="33", 
                    gallery_name="China and South Asia", 
                    qr_code_val="QR-8", 
                    clue_text="The goddess tara", 
                    silhouette_url="",
                    image_url="/images/artifact/The goddess tara.webp",
                    faction_id=asia.id
                ),
                ArtifactDB(
                    name="The Great Departure of Prince Siddhartha", 
                    room_no="33a", 
                    gallery_name="India :Amaravati", 
                    qr_code_val="QR-9", 
                    clue_text="The Great Departure of Prince Siddhartha", 
                    silhouette_url="",
                    image_url="/images/artifact/The Great Departure of Prince Siddhartha.jpg",
                    faction_id=asia.id
                ),
                ArtifactDB(
                    name="The Bacchic platter from the Mildenhall treasure", 
                    room_no="49", 
                    gallery_name="Roman Britain", 
                    qr_code_val="QR-10", 
                    clue_text="The Bacchic platter from the Mildenhall treasure", 
                    silhouette_url="",
                    image_url="/images/artifact/The Bacchic platter from the Mildenhall treasure.jpg",
                    faction_id=rome.id
                ),
                ArtifactDB(
                    name="Gold griffin-headed armlet", 
                    room_no="52", 
                    gallery_name="Ancient lran", 
                    qr_code_val="QR-11", 
                    clue_text="Gold griffin-headed armlet", 
                    silhouette_url="",
                    image_url="/images/artifact/Gold griffin-headed armlet.jpg",
                    faction_id=middle_east.id
                ),
                ArtifactDB(
                    name="Calcite incense burner showing a camel rider", 
                    room_no="53", 
                    gallery_name="Ancient South Arabia", 
                    qr_code_val="QR-12", 
                    clue_text="Calcite incense burner showing a camel rider", 
                    silhouette_url="",
                    image_url="/images/artifact/Calcite incense burner showing a camel rider.jpg",
                    faction_id=middle_east.id
                ),
                ArtifactDB(
                    name="Christian wall-painting", 
                    room_no="66", 
                    gallery_name="Ethiopia and Coptic Egypt", 
                    qr_code_val="QR-13", 
                    clue_text="Christian wall-painting", 
                    silhouette_url="",
                    image_url="/images/artifact/Christian wall-painting.jpg",
                    faction_id=egypt.id
                ),
                ArtifactDB(
                    name="White porcelain 'moon jar'", 
                    room_no="67", 
                    gallery_name="Korea", 
                    qr_code_val="QR-14", 
                    clue_text="White porcelain 'moon jar'", 
                    silhouette_url="",
                    image_url="/images/artifact/White porcelain 'moon jar'.webp",
                    faction_id=asia.id
                ),
                ArtifactDB(
                    name="Fragment of a stone panel from the South-West Palace of Sennacherib", 
                    room_no="9", 
                    gallery_name="Assyria: Nineveh", 
                    qr_code_val="QR-15", 
                    clue_text="Fragment of a stone panel from the South-West Palace of Sennacherib", 
                    silhouette_url="",
                    image_url="/images/artifact/Fragment of a stone panel from the South-West Palace of Sennacherib.jpg",
                    faction_id=middle_east.id
                ),
                ArtifactDB(
                    name="Carved jade terrapin, India", 
                    room_no="33", 
                    gallery_name="China and South Asia", 
                    qr_code_val="QR-16", 
                    clue_text="Carved jade terrapin", 
                    silhouette_url="",
                    image_url="/images/artifact/Carved jade terrapin, India.jpg",
                    faction_id=asia.id
                ),
            ]
            session.add_all(artifacts)
            session.commit()
            print("ดึงข้อมูล Artifacts ทั้งหมด 16 รายการลงฐานข้อมูลเรียบร้อยแล้ว")

# เริ่มต้นสร้างฐานข้อมูลและใส่ข้อมูลจำลอง
init_db()
seed_db()

app = FastAPI(title="Relic Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ระบบ Quiz Data & Persona
# ==========================================
@app.get('/quiz/questions', tags=["Quiz"])
def get_questions():
    """ดึงข้อมูลคำถามควิซจากไฟล์ JSON"""
    path = Path(__file__).resolve().parent.parent / 'src/lib/server/quiz-questions.json'
    with path.open(encoding='utf-8') as file:
        return json.load(file)

@app.post("/personas/quiz", tags=["Persona"])
async def persona_quiz_submit(answers: QuizAnswers):
    with Session(engine) as session:
        has_taken = session.exec(select(UserCollectionDB).where(UserCollectionDB.user_id == answers.user_id)).first()
        if has_taken:
            raise HTTPException(status_code=400, detail="คุณได้รับคอลเลกชันไปแล้ว!")

        user = session.exec(select(UserDB).where(UserDB.id == answers.user_id)).first()
        if not user:
            user = UserDB(id=answers.user_id, username="Explorer", email="test@example.com")
            session.add(user)
            session.commit()
            session.refresh(user)

        def get_code(ans):
            return "1" if ans == "like" else "2"
        
        pattern = f"{get_code(answers.ans_1)}{get_code(answers.ans_2)}{get_code(answers.ans_3)}{get_code(answers.ans_4)}{get_code(answers.ans_5)}"

        custom_rules = {
            "11111": "Colossal granite image of King Ramesses ll",
            "11112": "Brass head of an Ooni",
            "11121": "The Sutton hoo helmet",
            "11122": "The Portland Vase",
            "11211": "Bust of Sir Hans Sloane",
            "11212": "Relief panel from the Harpy Tomb",
            "11221": "Double-headed serpent mosaic",
            "11222": "The goddess tara",

            "12111": "The Great Departure of Prince Siddhartha",
            "12112": "The Bacchic platter from the Mildenhall treasure",
            "12121": "Gold griffin-headed armlet",
            "12122": "Calcite incense burner showing a camel rider",
            "12211": "Christian wall-painting",
            "12212": "White porcelain 'moon jar'",
            "12221": "Fragment of a stone panel from the South-West Palace of Sennacherib",
            "12222": "Carved jade terrapin, India",

            "21111": "Colossal granite image of King Ramesses ll",
            "21112": "Brass head of an Ooni",
            "21121": "The Sutton hoo helmet",
            "21122": "The Portland Vase",
            "21211": "Bust of Sir Hans Sloane",
            "21212": "Relief panel from the Harpy Tomb",
            "21221": "Double-headed serpent mosaic",
            "21222": "The goddess tara",

            "22111": "The Great Departure of Prince Siddhartha",
            "22112": "The Bacchic platter from the Mildenhall treasure",
            "22121": "Gold griffin-headed armlet",
            "22122": "Calcite incense burner showing a camel rider",
            "22211": "Christian wall-painting",
            "22212": "White porcelain 'moon jar'",
            "22221": "Fragment of a stone panel from the South-West Palace of Sennacherib",
            "22222": "Carved jade terrapin, India"
        }

        target_artifact_name = custom_rules.get(pattern)
        reward_artifact = session.exec(select(ArtifactDB).where(ArtifactDB.name == target_artifact_name)).first()

        if not reward_artifact:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล Artifact ในระบบ")

        faction = session.exec(select(FactionDB).where(FactionDB.id == reward_artifact.faction_id)).first()

        if not faction:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูล Faction ในระบบ")

        new_collection = UserCollectionDB(
            user_id=user.id,
            artifact_id=reward_artifact.id,
            scanned_at=datetime.now().isoformat(),
            is_collected=True,
        )
        session.add(new_collection)
        session.commit()

        return {
            "matched_faction": faction.name,
            "starting_artifact": reward_artifact.name,
            "image_url": reward_artifact.image_url
        }

# ==========================================
# ระบบ Clue Target (ล็อกเป้าหมายประจำตัว)
# ==========================================
@app.get("/clue/target/{user_id}", tags=["Clue"])
async def get_current_target(user_id: int):
    with Session(engine) as session:
        #เช็คว่าผู้ใช้มีบันทึกอยู่ใน UserCollectionDB หรือไม่ (ถ้าไม่มีแสดงว่ายังไม่ได้ทำ quiz)
        has_taken_quiz = session.exec(
            select(UserCollectionDB).where(UserCollectionDB.user_id == user_id)
        ).first()

        if not has_taken_quiz:
            return {
                "has_quiz": False,
                "completed": False,
                "message": "กรุณาทำ Quiz หรือกดสุ่มการ์ดเริ่มต้นก่อนเพื่อดูคำใบ้"
            }

        # 2. ดึงรายการ artifact ที่สะสมไปแล้ว
        collected_ids = session.exec(
            select(UserCollectionDB.artifact_id).where(UserCollectionDB.user_id == user_id)
        ).all()

        # 3. ค้นหา artifact ที่ยังไม่ได้สะสม
        uncollected = session.exec(
            select(ArtifactDB).where(ArtifactDB.id.not_in(collected_ids))
        ).all()

        if not uncollected:
            return {
                "has_quiz": True,
                "completed": True,
                "message": "คุณเก็บคอลเลกชันครบทั้งหมดแล้ว"
            }

        # ล็อกเป้าหมายใบแรกสุดในรายการที่ยังไม่ได้ปลดล็อก
        target = uncollected[0]

        return {
            "has_quiz": True,
            "completed": False,
            "artifact_id": target.id,
            "name": target.name,
            "clue_text": target.clue_text,
            "gallery_name": target.gallery_name,
            "room_no": target.room_no,
            "qr_code_val": target.qr_code_val
        }

# ==========================================
# ระบบ Artifacts (จัดการหลังบ้าน)
# ==========================================
@app.get("/artifacts/", tags=["Artifacts"])
async def get_all_artifacts():
    with Session(engine) as session:
        return session.exec(select(ArtifactDB)).all()

@app.post("/artifacts/", tags=["Artifacts"])
async def create_artifact(artifact: Artifact):
    with Session(engine) as session:
        new_artifact = ArtifactDB(**artifact.dict())
        session.add(new_artifact)
        session.commit()
        session.refresh(new_artifact)
        return new_artifact

# ==========================================
# ระบบ Collection (ดึงข้อมูลของสะสม)
# ==========================================
@app.get("/collections/by-user/{user_id}", tags=["Collection"], response_model=list[CollectionItemResponse])
async def collection_read_by_user(user_id: int):
    with Session(engine) as session:
        user = session.exec(select(UserDB).where(UserDB.id == user_id)).first()
        if not user:
            return []

        all_artifacts = session.exec(select(ArtifactDB)).all()
        collections = session.exec(select(UserCollectionDB).where(UserCollectionDB.user_id == user_id)).all()
        collected_map = {c.artifact_id: c.scanned_at for c in collections}

        result = []
        for artifact in all_artifacts:
            is_locked = artifact.id not in collected_map
            
            if is_locked:
                result.append(CollectionItemResponse(
                    artifact_id=artifact.id,
                    name="???", 
                    room_no=artifact.room_no,
                    gallery_name=artifact.gallery_name,
                    clue_text=artifact.clue_text,
                    image_url=None,
                    silhouette_url=artifact.silhouette_url,
                    is_locked=True,
                    scanned_at=None
                ))
            else:
                result.append(CollectionItemResponse(
                    artifact_id=artifact.id,
                    name=artifact.name,
                    room_no=artifact.room_no,
                    gallery_name=artifact.gallery_name,
                    clue_text=artifact.clue_text,
                    image_url=artifact.image_url,
                    silhouette_url=artifact.silhouette_url,
                    is_locked=False,
                    scanned_at=collected_map[artifact.id]
                ))
                
        return result

# ==========================================
# ระบบ Scan (ส่งโค้ดเพื่อปลดล็อก)
# ==========================================
@app.post("/collections/scan", tags=["Collection"])
async def scan_artifact(request: ScanRequest):
    with Session(engine) as session:
        artifact = session.exec(select(ArtifactDB).where(ArtifactDB.qr_code_val == request.qr_code_val)).first()
        if not artifact:
            raise HTTPException(status_code=404, detail="รหัสไม่ถูกต้อง หรือไม่พบสมบัตินี้")

        existing = session.exec(
            select(UserCollectionDB).where(
                UserCollectionDB.user_id == request.user_id,
                UserCollectionDB.artifact_id == artifact.id
            )
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="คุณปลดล็อกสมบัติชิ้นนี้ไปแล้ว")

        new_collection = UserCollectionDB(
            user_id=request.user_id,
            artifact_id=artifact.id,
            scanned_at=datetime.now().isoformat(),
            is_collected=True
        )
        session.add(new_collection)
        session.commit()

        return {"message": "ปลดล็อกสำเร็จ", "item": {"name": artifact.name}}