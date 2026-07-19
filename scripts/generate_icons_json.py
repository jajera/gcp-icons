#!/usr/bin/env python3
"""Generate icons.json from the organized Google Cloud SVG library."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
OUTPUT = ROOT / "icons.json"

TYPE_ORDER = {"category": 0, "product": 1, "legacy": 2}
TYPE_COLORS = {
    "category": "#4285F4",
    "product": "#4285F4",
    "legacy": "#4285F4",
}

CATEGORY_NAMES = {
    "agents": "AI Applications & Agents",
    "ai-machine-learning": "AI and Machine Learning",
    "business-intelligence": "Business Intelligence",
    "collaboration": "Collaboration",
    "compute": "Compute",
    "containers": "Containers",
    "data-analytics": "Data Analytics",
    "databases": "Databases",
    "developer-tools": "Developer Tools",
    "devops": "DevOps",
    "hybrid-and-multicloud": "Hybrid and Multicloud",
    "integration-services": "Integration Services",
    "management-tools": "Management Tools",
    "maps-and-geospatial": "Maps & Geospatial",
    "marketplace": "Marketplace",
    "media-services": "Media Services",
    "migration": "Migration",
    "mixed-reality": "Mixed Reality",
    "networking": "Networking",
    "observability": "Observability",
    "operations": "Operations",
    "security-identity": "Security and Identity",
    "serverless-computing": "Serverless",
    "storage": "Storage",
    "web-and-mobile": "Web and Mobile",
    "web3": "Web3",
}

PRODUCT_NAMES = {
    "ai-hypercomputer": "AI Hypercomputer",
    "alloydb": "AlloyDB",
    "anthos": "Anthos",
    "apigee": "Apigee",
    "bigquery": "BigQuery",
    "cloud-run": "Cloud Run",
    "cloud-spanner": "Spanner",
    "cloud-sql": "Cloud SQL",
    "cloud-storage": "Cloud Storage",
    "compute-engine": "Compute Engine",
    "distributed-cloud": "Google Distributed Cloud",
    "gke": "GKE",
    "hyperdisk": "Hyperdisk",
    "looker": "Looker",
    "mandiant": "Mandiant",
    "security-command-center": "Security Command Center",
    "security-operations": "Google Security Operations",
    "threat-intelligence": "Google Threat Intelligence",
    "vertex-ai": "Vertex AI",
}

LEGACY_NAMES = {
    "automl": "AutoML",
    "beyondcorp": "BeyondCorp",
    "bigquery": "BigQuery",
    "cloud-for-marketing": "Cloud for Marketing",
    "cloud-optimization-ai-fleet-routing-api": "Cloud Optimization AI - Fleet Routing API",
    "cloud-run-for-anthos": "Cloud Run for Anthos",
    "container-optimized-os": "Container-Optimized OS",
    "gke-on-prem": "GKE On-Prem",
    "identity-and-access-management": "Identity and Access Management",
    "identity-aware-proxy": "Identity-Aware Proxy",
    "kuberun": "KubeRun",
    "managed-service-for-microsoft-active-directory": (
        "Managed Service for Microsoft Active Directory"
    ),
    "migrate-for-anthos": "Migrate for Anthos",
    "migrate-for-compute-engine": "Migrate for Compute Engine",
    "pubsub": "Pub/Sub",
    "real-world-insights": "Real-World Insights",
    "speech-to-text": "Speech-to-Text",
    "tensorflow-enterprise": "TensorFlow Enterprise",
    "text-to-speech": "Text-to-Speech",
    "tools-for-powershell": "Cloud Tools for PowerShell",
    "vertexai": "Vertex AI",
}

TOKEN_NAMES = {
    "ai": "AI",
    "api": "API",
    "apis": "APIs",
    "automl": "AutoML",
    "cdn": "CDN",
    "cx": "CX",
    "dns": "DNS",
    "ekm": "EKM",
    "gce": "GCE",
    "gke": "GKE",
    "gpu": "GPU",
    "hsm": "HSM",
    "ids": "IDS",
    "iot": "IoT",
    "ip": "IP",
    "nat": "NAT",
    "nlp": "NLP",
    "os": "OS",
    "qna": "QnA",
    "sql": "SQL",
    "ssd": "SSD",
    "tpu": "TPU",
    "vmware": "VMware",
    "vpn": "VPN",
}

BRAND_NAMES = {
    "alloydb": "AlloyDB",
    "anthos": "Anthos",
    "apigee": "Apigee",
    "bigquery": "BigQuery",
    "bigtable": "Bigtable",
    "dataflow": "Dataflow",
    "datalab": "Datalab",
    "dataplex": "Dataplex",
    "datapol": "Datapol",
    "dataprep": "Dataprep",
    "dataproc": "Dataproc",
    "datashare": "Datashare",
    "datastore": "Datastore",
    "datastream": "Datastream",
    "dialogflow": "Dialogflow",
    "eventarc": "Eventarc",
    "filestore": "Filestore",
    "firestore": "Firestore",
    "looker": "Looker",
    "mandiant": "Mandiant",
    "memorystore": "Memorystore",
    "stackdriver": "Stackdriver",
}

EXTRA_TAGS = {
    "bigquery": ["bq"],
    "cloud-storage": ["gcs"],
    "compute-engine": ["gce", "vm", "virtual-machine"],
    "google-kubernetes-engine": ["gke", "kubernetes"],
    "identity-and-access-management": ["iam"],
    "pubsub": ["pub-sub", "messaging"],
    "virtual-private-cloud": ["vpc", "networking"],
}


def humanize(slug: str) -> str:
    words = []
    for word in slug.split("-"):
        words.append(TOKEN_NAMES.get(word, BRAND_NAMES.get(word, word.capitalize())))
    return " ".join(words)


def display_name(icon_type: str, slug: str) -> str:
    if icon_type == "category":
        return CATEGORY_NAMES.get(slug, humanize(slug))
    if icon_type == "product":
        return PRODUCT_NAMES.get(slug, humanize(slug))
    return LEGACY_NAMES.get(slug, humanize(slug))


def tags_for(icon_type: str, slug: str, fullname: str) -> list[str]:
    tags = {icon_type, "gcp", "google-cloud", slug}
    tags.update(re.findall(r"[a-z0-9]+", fullname.lower()))
    tags.update(EXTRA_TAGS.get(slug, []))
    return sorted(tags)


def description_for(icon_type: str, fullname: str) -> str:
    if icon_type == "category":
        return f"{fullname} category icon for Google Cloud products."
    if icon_type == "product":
        return f"{fullname} is a Google Cloud core product."
    return f"{fullname} legacy Google Cloud console icon."


def build_entries() -> list[dict[str, object]]:
    entries = []
    for svg_path in ICONS_DIR.glob("*/*/*.svg"):
        relative = svg_path.relative_to(ROOT)
        icon_type, slug = relative.parts[1:3]
        if icon_type not in TYPE_ORDER:
            continue
        fullname = display_name(icon_type, slug)
        entries.append(
            {
                "path": relative.as_posix(),
                "tags": tags_for(icon_type, slug, fullname),
                "category": icon_type,
                "color": TYPE_COLORS[icon_type],
                "description": description_for(icon_type, fullname),
                "fullname": fullname,
                "name": slug,
            }
        )

    entries.sort(
        key=lambda icon: (
            TYPE_ORDER[str(icon["category"])],
            str(icon["fullname"]).casefold(),
            str(icon["path"]),
        )
    )
    return entries


def main() -> None:
    entries = build_entries()
    if not entries:
        raise SystemExit(f"No SVG icons found under {ICONS_DIR}")

    OUTPUT.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} icons to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
