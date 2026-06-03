"""Receipt XML generation."""

from __future__ import annotations

import os
from datetime import datetime
from xml.etree import ElementTree as ET

from app.config import RECEIPTS_DIR


def generate_receipt_xml(data: dict) -> str:
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    root = ET.Element("receipt")
    ET.SubElement(root, "purchase_id").text = str(data.get("_id", ""))
    ET.SubElement(root, "user").text = data.get("user_name", "")
    ET.SubElement(root, "movie").text = data.get("movie_name", "")
    ET.SubElement(root, "schedule").text = data.get("schedule", "")
    ET.SubElement(root, "quantity").text = str(data.get("quantity", 0))
    ET.SubElement(root, "total").text = f"{data.get('total', 0):.2f}"
    ET.SubElement(root, "purchased_at").text = data.get("purchased_at", datetime.utcnow()).isoformat()

    tree = ET.ElementTree(root)
    filename = f"receipt_{data.get('_id', 'unknown')}.xml"
    path = os.path.join(RECEIPTS_DIR, filename)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path
