-- CBSE portal demonstration seed data.
-- All records below are representative DEMO data and are not sourced from live CBSE publications.

-- circulars
insert into public.circulars (
  id,
  title,
  description,
  content,
  category,
  target_audience,
  publish_date,
  document_url,
  source_url
) values
  (
    '51000000-0000-4000-8000-000000000001',
    '[DEMO] Examination Circular: Class X and XII Annual Examination Guidelines',
    'Representative examination guidance for schools, students, and parents.',
    'DEMONSTRATION DATA ONLY. This sample circular outlines how examination schedules, candidate instructions, and school coordination notices could be presented on the portal.',
    'Examinations', array['Students', 'Parents', 'Schools'], '2026-08-26 09:00:00+05:30',
    'https://demo.cbse.example/documents/examination-guidelines-2026.pdf',
    'https://demo.cbse.example/circulars/examination-guidelines-2026'
  ),
  (
    '51000000-0000-4000-8000-000000000002',
    '[DEMO] Result Services Notice: Verification and Re-evaluation Process',
    'Representative post-result service notice for eligible candidates.',
    'DEMONSTRATION DATA ONLY. This sample describes a verification and re-evaluation workflow; actual eligibility, fees, and dates must be published through official channels.',
    'Results', array['Students', 'Parents'], '2026-08-24 10:00:00+05:30',
    'https://demo.cbse.example/documents/result-services-notice-2026.pdf',
    'https://demo.cbse.example/circulars/result-services-notice-2026'
  ),
  (
    '51000000-0000-4000-8000-000000000003',
    '[DEMO] Academic Circular: Curriculum Enrichment Activities for 2026–27',
    'Representative academic update for curriculum enrichment planning.',
    'DEMONSTRATION DATA ONLY. Schools may use this sample to understand how curriculum-related guidance, resource links, and implementation notes could appear.',
    'Academics', array['Teachers', 'Principals', 'Schools'], '2026-08-21 11:30:00+05:30',
    'https://demo.cbse.example/documents/curriculum-enrichment-2026-27.pdf',
    'https://demo.cbse.example/circulars/curriculum-enrichment-2026-27'
  ),
  (
    '51000000-0000-4000-8000-000000000004',
    '[DEMO] Student Services Circular: Digital Academic Document Requests',
    'Representative information about requesting academic records and certificates.',
    'DEMONSTRATION DATA ONLY. This sample shows the type of instructions that may be provided for digital academic document and certificate services.',
    'Student Services', array['Students', 'Parents'], '2026-08-19 14:00:00+05:30',
    'https://demo.cbse.example/documents/digital-document-requests.pdf',
    'https://demo.cbse.example/circulars/digital-document-requests'
  ),
  (
    '51000000-0000-4000-8000-000000000005',
    '[DEMO] CTET Notice: Information Bulletin and Candidate Support',
    'Representative CTET information notice for prospective candidates.',
    'DEMONSTRATION DATA ONLY. This sample illustrates an information-bulletin update with candidate support guidance and reference links.',
    'CTET', array['Students', 'Teachers', 'Candidates'], '2026-08-17 09:45:00+05:30',
    'https://demo.cbse.example/documents/ctet-information-bulletin.pdf',
    'https://demo.cbse.example/circulars/ctet-information-bulletin'
  ),
  (
    '51000000-0000-4000-8000-000000000006',
    '[DEMO] General Notice: Safe and Inclusive School Practices',
    'Representative general notice for school administration and staff.',
    'DEMONSTRATION DATA ONLY. This sample contains generic guidance on maintaining safe, inclusive, and supportive learning environments.',
    'General Notices', array['Schools', 'Principals', 'Teachers'], '2026-08-15 12:15:00+05:30',
    'https://demo.cbse.example/documents/safe-inclusive-school-practices.pdf',
    'https://demo.cbse.example/circulars/safe-inclusive-school-practices'
  ),
  (
    '51000000-0000-4000-8000-000000000007',
    '[DEMO] Examination Update: Sample Question Papers and Marking Schemes',
    'Representative resource update for examination preparation.',
    'DEMONSTRATION DATA ONLY. This sample shows how a circular can link students and teachers to practice materials and explanatory marking guidance.',
    'Examinations', array['Students', 'Teachers', 'Parents'], '2026-08-12 10:30:00+05:30',
    'https://demo.cbse.example/documents/sample-question-papers-2026.pdf',
    'https://demo.cbse.example/circulars/sample-question-papers-2026'
  ),
  (
    '51000000-0000-4000-8000-000000000008',
    '[DEMO] Results Notice: Supplementary Examination Result Support',
    'Representative notice covering result access and follow-up support.',
    'DEMONSTRATION DATA ONLY. This sample demonstrates a concise result notice with pointers for document services and further assistance.',
    'Results', array['Students', 'Parents', 'Schools'], '2026-08-09 15:00:00+05:30',
    'https://demo.cbse.example/documents/supplementary-result-support.pdf',
    'https://demo.cbse.example/circulars/supplementary-result-support'
  ),
  (
    '51000000-0000-4000-8000-000000000009',
    '[DEMO] Academic Notice: Capacity Building Programme for Science Teachers',
    'Representative professional-development notice for science teachers.',
    'DEMONSTRATION DATA ONLY. This sample describes a potential capacity-building programme and the type of registration guidance a circular may contain.',
    'Academics', array['Teachers', 'Schools'], '2026-08-06 11:00:00+05:30',
    'https://demo.cbse.example/documents/science-teacher-capacity-building.pdf',
    'https://demo.cbse.example/circulars/science-teacher-capacity-building'
  ),
  (
    '51000000-0000-4000-8000-000000000010',
    '[DEMO] General Notice: School Data Verification Window',
    'Representative administrative notice for affiliated institutions.',
    'DEMONSTRATION DATA ONLY. This sample shows how the portal can communicate a school data-review window and related support information.',
    'General Notices', array['Schools', 'Principals'], '2026-08-03 09:30:00+05:30',
    'https://demo.cbse.example/documents/school-data-verification-window.pdf',
    'https://demo.cbse.example/circulars/school-data-verification-window'
  )
on conflict (id) do update set
  title = excluded.title,
  description = excluded.description,
  content = excluded.content,
  category = excluded.category,
  target_audience = excluded.target_audience,
  publish_date = excluded.publish_date,
  document_url = excluded.document_url,
  source_url = excluded.source_url;

-- news
insert into public.news (
  id,
  title,
  description,
  category,
  publish_date,
  source_url
) values
  (
    '52000000-0000-4000-8000-000000000001',
    '[DEMO] Examination Update: Board Examination Preparation Resources',
    'Representative announcement about access to examination-preparation resources for students and schools.',
    'Examinations', '2026-08-25 10:00:00+05:30',
    'https://demo.cbse.example/news/examination-preparation-resources'
  ),
  (
    '52000000-0000-4000-8000-000000000002',
    '[DEMO] Academic Update: Digital Learning Resource Collection Released',
    'Representative news item demonstrating an academic-resource announcement for secondary classes.',
    'Academics', '2026-08-22 11:30:00+05:30',
    'https://demo.cbse.example/news/digital-learning-resources'
  ),
  (
    '52000000-0000-4000-8000-000000000003',
    '[DEMO] Results Announcement: Post-Result Support Information',
    'Representative update outlining where candidates can find post-result service guidance.',
    'Results', '2026-08-20 14:00:00+05:30',
    'https://demo.cbse.example/news/post-result-support'
  ),
  (
    '52000000-0000-4000-8000-000000000004',
    '[DEMO] General Announcement: Inclusive Education Awareness Week',
    'Representative public-awareness announcement for schools, teachers, students, and families.',
    'General', '2026-08-18 09:45:00+05:30',
    'https://demo.cbse.example/news/inclusive-education-awareness-week'
  ),
  (
    '52000000-0000-4000-8000-000000000005',
    '[DEMO] Careers Notice: Recruitment Information Helpdesk',
    'Representative careers-related notice showing how application assistance details may be presented.',
    'Careers', '2026-08-15 12:15:00+05:30',
    'https://demo.cbse.example/news/recruitment-information-helpdesk'
  ),
  (
    '52000000-0000-4000-8000-000000000006',
    '[DEMO] Examination News: School Coordination Meeting Schedule',
    'Representative update for schools regarding examination-readiness coordination activities.',
    'Examinations', '2026-08-12 15:30:00+05:30',
    'https://demo.cbse.example/news/school-coordination-meeting'
  ),
  (
    '52000000-0000-4000-8000-000000000007',
    '[DEMO] Academic Announcement: Science Innovation Showcase',
    'Representative announcement about a student-focused science and innovation showcase.',
    'Academics', '2026-08-09 10:15:00+05:30',
    'https://demo.cbse.example/news/science-innovation-showcase'
  ),
  (
    '52000000-0000-4000-8000-000000000008',
    '[DEMO] General Update: School Sports Participation Information',
    'Representative update describing the type of sports participation information available to schools.',
    'General', '2026-08-06 13:00:00+05:30',
    'https://demo.cbse.example/news/school-sports-participation'
  )
on conflict (id) do update set
  title = excluded.title,
  description = excluded.description,
  category = excluded.category,
  publish_date = excluded.publish_date,
  source_url = excluded.source_url;

-- important_dates

-- services
insert into public.services (
  id,
  title,
  description,
  category,
  target_audience,
  url,
  icon
) values
  (
    '53000000-0000-4000-8000-000000000001',
    '[DEMO] Results Portal',
    'Representative entry point for viewing examination results and result-related notices.',
    'Results', array['Students', 'Parents', 'Schools'],
    'https://demo.cbse.example/services/results', 'chart-line'
  ),
  (
    '53000000-0000-4000-8000-000000000002',
    '[DEMO] Admit Card Services',
    'Representative access point for admit-card instructions and candidate support.',
    'Examinations', array['Students', 'Parents', 'Schools'],
    'https://demo.cbse.example/services/admit-card', 'ticket-alt'
  ),
  (
    '53000000-0000-4000-8000-000000000003',
    '[DEMO] Migration Certificate',
    'Representative service for migration-certificate information and requests.',
    'Student Services', array['Students', 'Parents'],
    'https://demo.cbse.example/services/migration-certificate', 'file-signature'
  ),
  (
    '53000000-0000-4000-8000-000000000004',
    '[DEMO] Duplicate Academic Documents',
    'Representative service for duplicate mark sheets, certificates, and related documents.',
    'Student Services', array['Students', 'Parents'],
    'https://demo.cbse.example/services/duplicate-documents', 'copy'
  ),
  (
    '53000000-0000-4000-8000-000000000005',
    '[DEMO] Academic Resources',
    'Representative access point for curriculum resources, sample papers, and learning materials.',
    'Academics', array['Students', 'Teachers', 'Parents'],
    'https://demo.cbse.example/services/academic-resources', 'book-open'
  ),
  (
    '53000000-0000-4000-8000-000000000006',
    '[DEMO] CBSE School Locator',
    'Representative school-search service for families and education stakeholders.',
    'School Services', array['Parents', 'Students', 'Schools'],
    'https://demo.cbse.example/services/school-locator', 'school'
  ),
  (
    '53000000-0000-4000-8000-000000000007',
    '[DEMO] Examination Services',
    'Representative hub for examination schedules, forms, and candidate guidance.',
    'Examinations', array['Students', 'Parents', 'Schools', 'Teachers'],
    'https://demo.cbse.example/services/examinations', 'clipboard-check'
  ),
  (
    '53000000-0000-4000-8000-000000000008',
    '[DEMO] Student Support Services',
    'Representative hub for student-facing certificates, scholarships, and support information.',
    'Student Services', array['Students', 'Parents'],
    'https://demo.cbse.example/services/student-support', 'user-graduate'
  )
on conflict (id) do update set
  title = excluded.title,
  description = excluded.description,
  category = excluded.category,
  target_audience = excluded.target_audience,
  url = excluded.url,
  icon = excluded.icon;
