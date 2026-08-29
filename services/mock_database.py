import re
from datetime import datetime

CIRCULARS = [
    {
        "id": "51000000-0000-4000-8000-000000000001",
        "title": "[DEMO] Examination Circular: Class X and XII Annual Examination Guidelines",
        "description": "Representative examination guidance for schools, students, and parents.",
        "content": "DEMONSTRATION DATA ONLY. This sample circular outlines how examination schedules, candidate instructions, and school coordination notices could be presented on the portal.",
        "category": "Examinations",
        "target_audience": ["Students", "Parents", "Schools"],
        "publish_date": "2026-08-26T09:00:00+05:30",
        "document_url": "https://demo.cbse.example/documents/examination-guidelines-2026.pdf",
        "source_url": "https://demo.cbse.example/circulars/examination-guidelines-2026",
        "created_at": "2026-08-26T09:00:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000002",
        "title": "[DEMO] Result Services Notice: Verification and Re-evaluation / Revaluation Process",
        "description": "Representative post-result service notice for eligible candidates regarding marks verification and revaluation.",
        "content": "DEMONSTRATION DATA ONLY. This sample describes a verification and revaluation / re-evaluation workflow; actual eligibility, fees, and dates must be published through official channels.",
        "category": "Results",
        "target_audience": ["Students", "Parents"],
        "publish_date": "2026-08-24T10:00:00+05:30",
        "document_url": "https://demo.cbse.example/documents/result-services-notice-2026.pdf",
        "source_url": "https://demo.cbse.example/circulars/result-services-notice-2026",
        "created_at": "2026-08-24T10:00:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000003",
        "title": "[DEMO] Academic Circular: Curriculum Enrichment Activities for 2026–27",
        "description": "Representative academic update for curriculum enrichment planning.",
        "content": "DEMONSTRATION DATA ONLY. Schools may use this sample to understand how curriculum-related guidance, resource links, and implementation notes could appear.",
        "category": "Academics",
        "target_audience": ["Teachers", "Principals", "Schools"],
        "publish_date": "2026-08-21T11:30:00+05:30",
        "document_url": "https://demo.cbse.example/documents/curriculum-enrichment-2026-27.pdf",
        "source_url": "https://demo.cbse.example/circulars/curriculum-enrichment-2026-27",
        "created_at": "2026-08-21T11:30:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000004",
        "title": "[DEMO] Student Services Circular: Digital Academic Document and Migration Certificate Requests",
        "description": "Representative information about requesting academic records, migration certificates, and duplicate marksheets.",
        "content": "DEMONSTRATION DATA ONLY. This sample shows the instructions provided for digital academic documents, duplicate certificates, and migration certificate applications.",
        "category": "Student Services",
        "target_audience": ["Students", "Parents"],
        "publish_date": "2026-08-19T14:00:00+05:30",
        "document_url": "https://demo.cbse.example/documents/digital-document-requests.pdf",
        "source_url": "https://demo.cbse.example/circulars/digital-document-requests",
        "created_at": "2026-08-19T14:00:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000005",
        "title": "[DEMO] CTET Notice: Information Bulletin and Candidate Support",
        "description": "Representative CTET (Central Teacher Eligibility Test) information notice for prospective candidates.",
        "content": "DEMONSTRATION DATA ONLY. This sample illustrates a CTET information-bulletin update with candidate support guidance, syllabus details, and reference links.",
        "category": "CTET",
        "target_audience": ["Students", "Teachers", "Candidates"],
        "publish_date": "2026-08-17T09:45:00+05:30",
        "document_url": "https://demo.cbse.example/documents/ctet-information-bulletin.pdf",
        "source_url": "https://demo.cbse.example/circulars/ctet-information-bulletin",
        "created_at": "2026-08-17T09:45:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000006",
        "title": "[DEMO] Examination Update: Admit Card Distribution Guidance",
        "description": "Representative notice for school and candidate admit card downloading workflows.",
        "content": "DEMONSTRATION DATA ONLY. Schools should download and distribute verified admit cards to candidates prior to the examination period.",
        "category": "Examinations",
        "target_audience": ["Students", "Schools", "Parents"],
        "publish_date": "2026-08-20T12:00:00+05:30",
        "document_url": "https://demo.cbse.example/documents/admit-card-guidance.pdf",
        "source_url": "https://demo.cbse.example/circulars/admit-card-guidance",
        "created_at": "2026-08-20T12:00:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000007",
        "title": "[DEMO] Examination Update: Sample Question Papers and Marking Schemes",
        "description": "Representative resource update for examination preparation.",
        "content": "DEMONSTRATION DATA ONLY. This sample shows how a circular can link students and teachers to practice materials and explanatory marking guidance.",
        "category": "Examinations",
        "target_audience": ["Students", "Teachers", "Parents"],
        "publish_date": "2026-08-12T10:30:00+05:30",
        "document_url": "https://demo.cbse.example/documents/sample-question-papers-2026.pdf",
        "source_url": "https://demo.cbse.example/circulars/sample-question-papers-2026",
        "created_at": "2026-08-12T10:30:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000008",
        "title": "[DEMO] Results Notice: Supplementary Examination Result Support",
        "description": "Representative notice covering board examination results access, revaluation procedures, and follow-up support.",
        "content": "DEMONSTRATION DATA ONLY. This sample demonstrates a concise result notice with pointers for document services, revaluation, and further assistance.",
        "category": "Results",
        "target_audience": ["Students", "Parents", "Schools"],
        "publish_date": "2026-08-09T15:00:00+05:30",
        "document_url": "https://demo.cbse.example/documents/supplementary-result-support.pdf",
        "source_url": "https://demo.cbse.example/circulars/supplementary-result-support",
        "created_at": "2026-08-09T15:00:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000009",
        "title": "[DEMO] General Notice: Safe and Inclusive School Practices",
        "description": "Representative general notice for school administration and staff.",
        "content": "DEMONSTRATION DATA ONLY. This sample contains generic guidance on maintaining safe, inclusive, and supportive learning environments.",
        "category": "General Notices",
        "target_audience": ["Schools", "Principals", "Teachers"],
        "publish_date": "2026-08-15T12:15:00+05:30",
        "document_url": None,
        "source_url": None,
        "created_at": "2026-08-15T12:15:00+05:30",
    },
    {
        "id": "51000000-0000-4000-8000-000000000010",
        "title": "[DEMO] General Notice: School Data Verification Window",
        "description": "Representative administrative notice for affiliated institutions.",
        "content": "DEMONSTRATION DATA ONLY. This sample shows how the portal can communicate a school data-review window and related support information.",
        "category": "General Notices",
        "target_audience": ["Schools", "Principals"],
        "publish_date": "2026-08-03T09:30:00+05:30",
        "document_url": None,
        "source_url": None,
        "created_at": "2026-08-03T09:30:00+05:30",
    }
]

NEWS = [
    {
        "id": "52000000-0000-4000-8000-000000000001",
        "title": "[DEMO] Examination Update: Board Examination Preparation Resources",
        "description": "Representative announcement about access to examination-preparation resources for students and schools.",
        "category": "Examinations",
        "publish_date": "2026-08-25T10:00:00+05:30",
        "source_url": "https://demo.cbse.example/news/examination-preparation-resources",
        "created_at": "2026-08-25T10:00:00+05:30",
    },
    {
        "id": "52000000-0000-4000-8000-000000000002",
        "title": "[DEMO] Academic Update: Digital Learning Resource Collection Released",
        "description": "Representative news item demonstrating an academic-resource announcement for secondary classes.",
        "category": "Academics",
        "publish_date": "2026-08-22T11:30:00+05:30",
        "source_url": "https://demo.cbse.example/news/digital-learning-resources",
        "created_at": "2026-08-22T11:30:00+05:30",
    },
    {
        "id": "52000000-0000-4000-8000-000000000003",
        "title": "[DEMO] Results Announcement: Post-Result Support and Revaluation Helpdesk",
        "description": "Representative update outlining where candidates can find post-result service and revaluation guidance.",
        "category": "Results",
        "publish_date": "2026-08-20T14:00:00+05:30",
        "source_url": "https://demo.cbse.example/news/post-result-support",
        "created_at": "2026-08-20T14:00:00+05:30",
    },
    {
        "id": "52000000-0000-4000-8000-000000000004",
        "title": "[DEMO] General Announcement: Inclusive Education Awareness Week",
        "description": "Representative public-awareness announcement for schools, teachers, students, and families.",
        "category": "General",
        "publish_date": "2026-08-18T09:45:00+05:30",
        "source_url": "https://demo.cbse.example/news/inclusive-education-awareness-week",
        "created_at": "2026-08-18T09:45:00+05:30",
    },
    {
        "id": "52000000-0000-4000-8000-000000000005",
        "title": "[DEMO] CTET Update: Candidate Support and Schedule Information",
        "description": "Representative news item covering CTET candidate assistance and schedule updates.",
        "category": "CTET",
        "publish_date": "2026-08-16T12:00:00+05:30",
        "source_url": "https://demo.cbse.example/news/ctet-candidate-support",
        "created_at": "2026-08-16T12:00:00+05:30",
    }
]

IMPORTANT_DATES = [
    {
        "id": "53000000-0000-4000-8000-000000000001",
        "title": "[DEMO] Post-Result Services & Revaluation Application Deadline",
        "description": "Representative deadline for post-result service and revaluation applications.",
        "event_date": "2026-08-28",
        "category": "Results",
        "target_audience": ["Students", "Parents"],
        "source_url": None,
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "53000000-0000-4000-8000-000000000002",
        "title": "[DEMO] Admit Card Download Window for Supplementary Exams",
        "description": "Representative admit card download schedule for schools and students.",
        "event_date": "2026-09-05",
        "category": "Examinations",
        "target_audience": ["Students", "Schools"],
        "source_url": None,
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "53000000-0000-4000-8000-000000000003",
        "title": "[DEMO] CTET Online Application Form Submission Opens",
        "description": "Representative date for CTET registration.",
        "event_date": "2026-09-12",
        "category": "CTET",
        "target_audience": ["Candidates", "Teachers"],
        "source_url": None,
        "created_at": "2026-08-28T00:00:00+05:30",
    }
]

SERVICES = [
    {
        "id": "54000000-0000-4000-8000-000000000001",
        "title": "[DEMO] Results Portal",
        "description": "Representative entry point for viewing examination results, marks verification, and result-related notices.",
        "category": "Results",
        "target_audience": ["Students", "Parents", "Schools"],
        "url": "https://demo.cbse.example/services/results",
        "icon": "chart-line",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000002",
        "title": "[DEMO] Admit Card Services",
        "description": "Representative access point for admit card instructions, downloads, and candidate examination support.",
        "category": "Examinations",
        "target_audience": ["Students", "Parents", "Schools"],
        "url": "https://demo.cbse.example/services/admit-card",
        "icon": "ticket-alt",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000003",
        "title": "[DEMO] Migration Certificate Services",
        "description": "Representative service for migration certificate information, applications, and digital document requests.",
        "category": "Student Services",
        "target_audience": ["Students", "Parents"],
        "url": "https://demo.cbse.example/services/migration-certificate",
        "icon": "file-signature",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000004",
        "title": "[DEMO] Re-evaluation / Revaluation Portal",
        "description": "Representative portal for marks verification, photocopy of answer books, and revaluation services.",
        "category": "Results",
        "target_audience": ["Students", "Parents"],
        "url": "https://demo.cbse.example/services/revaluation",
        "icon": "search",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000005",
        "title": "[DEMO] Central Teacher Eligibility Test (CTET) Portal",
        "description": "Representative official portal for CTET notifications, eligibility criteria, and candidate applications.",
        "category": "CTET",
        "target_audience": ["Teachers", "Candidates"],
        "url": "https://ctet.nic.in",
        "icon": "id-badge",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000006",
        "title": "[DEMO] Duplicate Academic Documents (DADS)",
        "description": "Representative service for duplicate mark sheets, passing certificates, and migration documents.",
        "category": "Student Services",
        "target_audience": ["Students", "Parents"],
        "url": "https://demo.cbse.example/services/duplicate-documents",
        "icon": "copy",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000007",
        "title": "[DEMO] Academic Resources",
        "description": "Representative access point for curriculum resources, sample papers, and learning materials.",
        "category": "Academics",
        "target_audience": ["Students", "Teachers", "Parents"],
        "url": "https://demo.cbse.example/services/academic-resources",
        "icon": "book-open",
        "created_at": "2026-08-28T00:00:00+05:30",
    },
    {
        "id": "54000000-0000-4000-8000-000000000008",
        "title": "[DEMO] CBSE School Locator",
        "description": "Representative school-search service for families and education stakeholders.",
        "category": "School Services",
        "target_audience": ["Parents", "Students", "Schools"],
        "url": "https://demo.cbse.example/services/school-locator",
        "icon": "school",
        "created_at": "2026-08-28T00:00:00+05:30",
    }
]

TABLE_MAP = {
    "circulars": CIRCULARS,
    "news": NEWS,
    "important_dates": IMPORTANT_DATES,
    "services": SERVICES,
}


class MockSupabaseResponse:
    def __init__(self, data):
        self.data = data


class MockQueryBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
        self.data = list(TABLE_MAP.get(table_name, []))

    def select(self, fields="*"):
        return self

    def eq(self, column, value):
        self.data = [
            row
            for row in self.data
            if str(row.get(column)).lower() == str(value).lower()
        ]
        return self

    def ilike(self, column, pattern):
        # Extract query text inside %...%
        raw_pattern = pattern.strip("%")
        escaped_pattern = re.escape(raw_pattern)
        regex = re.compile(f".*{escaped_pattern}.*", re.IGNORECASE)
        self.data = [
            row
            for row in self.data
            if row.get(column) and regex.search(str(row.get(column)))
        ]
        return self

    def order(self, column, desc=True):
        def sort_key(row):
            val = row.get(column)
            if not val:
                return ""
            return val

        self.data.sort(key=sort_key, reverse=desc)
        return self

    def limit(self, count):
        self.data = self.data[:count]
        return self

    def contains(self, column, value):
        """Filter rows where the column list contains ALL items in *value*."""
        if not isinstance(value, list):
            value = [value]
        value_lower = [str(v).lower() for v in value]
        self.data = [
            row
            for row in self.data
            if all(
                any(str(item).lower() == needle for item in (row.get(column) or []))
                for needle in value_lower
            )
        ]
        return self

    def execute(self):
        return MockSupabaseResponse(self.data)



class MockSupabaseClient:
    def table(self, table_name):
        return MockQueryBuilder(table_name)
