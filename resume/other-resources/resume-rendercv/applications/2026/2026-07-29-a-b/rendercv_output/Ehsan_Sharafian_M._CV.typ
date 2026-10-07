// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.3.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Ehsan Sharafian M.",
  title: "Ehsan Sharafian M. - CV",
  footer: context { [#emph[Ehsan Sharafian M. -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in July 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "us-letter",
  page-top-margin: 1.27cm,
  page-bottom-margin: 1.27cm,
  page-left-margin: 1.27cm,
  page-right-margin: 1.27cm,
  page-show-footer: false,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 74, 109),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 74, 109),
  colors-section-titles: rgb(0, 74, 109),
  colors-links: rgb(0, 74, 109),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Source Sans 3",
  typography-font-family-name: "Source Sans 3",
  typography-font-family-headline: "Source Sans 3",
  typography-font-family-connections: "Source Sans 3",
  typography-font-family-section-titles: "Source Sans 3",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_partial_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: true,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0.15cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 7,
    day: 29,
  ),
)


= Ehsan Sharafian M.

#connections(
  [#connection-with-icon("location-dot")[Orono, ME]],
  [#link("mailto:ehsan.sharafian@maine.edu", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[ehsan.sharafian\@maine.edu]]],
  [#link("tel:+1-207-631-6979", icon: false, if-underline: false, if-color: false)[#connection-with-icon("phone")[(207) 631-6979]]],
  [#link("https://ehsansharafian.com/", icon: false, if-underline: false, if-color: false)[#connection-with-icon("link")[ehsansharafian.com]]],
  [#link("https://linkedin.com/in/ehsan-sharafian-m", icon: false, if-underline: false, if-color: false)[#connection-with-icon("linkedin")[ehsan-sharafian-m]]],
  [#link("https://github.com/ehsansharafianm", icon: false, if-underline: false, if-color: false)[#connection-with-icon("github")[ehsansharafianm]]],
)


== Professional Summary

Mechanical Engineering PhD candidate specializing in intelligent wearable systems for human movement analysis and digital health. Experienced in building end-to-end solutions that integrate IMU-based sensing, embedded hardware, smartphone applications, machine learning, and haptic feedback for gait analysis and rehabilitation. Skilled in Python, MATLAB, Android Studio\/Java, and PyTorch, with six peer-reviewed journal publications.

== Education

#education-entry(
  [
    #strong[University of Maine], Mechanical Engineering

    - GPA: 4.00\/4.00

    - Dissertation: Smart Real-Time Gait Training System

  ],
  [
    Orono, ME

    Expected Dec 2027

  ],
  degree-column: [
    #strong[PhD]
  ],
)

#education-entry(
  [
    #strong[Amirkabir University of Technology (Tehran Polytechnic)], Mechanical Engineering

    - GPA: 3.65\/4.00

    - Thesis: Trajectory optimization of a robot arm in joint and Cartesian spaces

  ],
  [
    Feb 2020

  ],
  degree-column: [
    #strong[MS]
  ],
)

#education-entry(
  [
    #strong[University of Tehran], Mechanical Engineering

  ],
  [
    Jul 2017

  ],
  degree-column: [
    #strong[BS]
  ],
)

== Technical Skills

#strong[Programming & Data Analysis:] Python, Java, C\/C++, NumPy, Pandas, scikit-learn, PyTorch, SPSS

#strong[Mobile & Software:] MATLAB, Simulink, TwinCAT, Android Studio, Unity, Git

#strong[Wearable & Embedded Systems:] IMU sensors, Arduino IDE, SparkFun modules, vibrotactile motors, PCB modules

#strong[Biomechanics & Signal Processing:] Gait analysis, human activity recognition, sensor fusion, feature extraction, OpenSim

#strong[Robotics:] Surgical robotics, parallel manipulators, inverse kinematics, dynamics, control systems

#strong[CAD:] SolidWorks

== Research & Engineering Experience

#regular-entry(
  [
    #strong[Graduate Research Assistant], Biorobotics and Biomechanics Lab, University of Maine

    - Led the development of real-time wearable sensing systems and Android-based mobile applications for gait analysis, activity recognition, fall-risk assessment, and home-based rehabilitation using IMUs, haptic feedback, and smartphone-deployed feedback platforms.

    - Built a smartphone-deployed gait assessment system using a single foot-mounted IMU to reconstruct foot-height trajectories, achieving #strong[96.08\% locomotion classification accuracy], #strong[less than 1.1 cm cumulative height error], and #strong[112 ms latency].

    - Engineered a lightweight human activity recognition system using two IMUs, biomechanical feature extraction, and supervised classifiers including SVM and Naive Bayes, achieving #strong[99.1\% accuracy] for normal locomotion and #strong[93.1\% accuracy] for atypical stair-negotiation strategies in older adults.

    - Architected a home-based haptic feedback gait-training system integrating IMUs, vibrotactile motors, custom Android applications, Arduino\/SparkFun modules, and PCB circuitry for adults aged 65+.

    - Demonstrated up to #strong[30\% improvement] in stride length and walking speed during a single-session haptic feedback study, with minimal cognitive demand.

    - Led IRB-approved human-subject validation studies with #strong[85+ participants] across gait analysis, activity recognition, and haptic feedback protocols.

    - Developed real-time algorithms and data pipelines in Android Studio\/Java, Python, and MATLAB, combining signal processing, sensor fusion, biomechanical modeling, and machine learning for mobile health applications.

  ],
  [
    Orono, ME

    Sept 2023 – present

  ],
)

#regular-entry(
  [
    #strong[Mechanical and Control Systems Engineer], Sina Robotics and Medical Innovators Co.

    - Developed PLC-based control logic for a telesurgical laparoscopic robotic platform using Beckhoff TwinCAT and IEC 61131-3 Structured Text, with MATLAB\/Simulink validation of inverse kinematics and initialization workflows.

    - Built a Python\/Kivy graphical user interface on Raspberry Pi for surgeon-facing robot control, system guidance, warnings, and improved human-robot interaction during testing and demonstrations.

    - Coordinated hands-on validation sessions with #strong[6 experienced surgeons], using training, troubleshooting, and usability feedback to refine surgeon-facing robotic system workflows.

  ],
  [
    Tehran, Iran

    Dec 2022 – Sept 2023

  ],
)

#regular-entry(
  [
    #strong[Laboratory Research Assistant], New Technology Research Center, Amirkabir University of Technology

    - Designed and assembled robotics and mechatronics setups for student research projects, integrating hardware, CAD, MATLAB workflows, and technical documentation.

    - Mentored #strong[6 undergraduate students] across #strong[5 research teams], guiding equipment use, troubleshooting, documentation, and project execution.

    - Coordinated technical preparation for the #strong[9th International Conference on Robotics and Mechatronics], including lab demonstrations, equipment readiness, and presentation logistics.

  ],
  [
    Tehran, Iran

    Nov 2020 – Nov 2022

  ],
)

== Selected Honors

#regular-entry(
  [
    #strong[Flagship Fellowship Award, University of Maine]

  ],
  [
    Sep 2024 – Sep 2025

  ],
)

#regular-entry(
  [
    #strong[Graduate Student Government Award for conference proposal]

  ],
  [
    Mar 2025

  ],
)

== Leadership & Service

#regular-entry(
  [
    #strong[Graduate Senator], Department of Mechanical Engineering, University of Maine

  ],
  [
    Sept 2025 – present

  ],
)

#regular-entry(
  [
    #strong[President], Iranian Graduate Student Association, University of Maine

  ],
  [
    Sept 2024 – Apr 2026

  ],
)

== Publications

- #strong[6 peer-reviewed journal articles] (3 first-author) in wearable sensing, biomechanics, rehabilitation engineering, and robotics.

- #strong[Sensors] (2026) – Real-time foot-height estimation and activity classification

- #strong[IEEE Access] (2025) – Lightweight IMU-based activity recognition for older adults

- #strong[IEEE TNSRE] (2025) – Haptic feedback effects on gait and cognitive load

- #strong[Journal of Biomechanics] (2025) – Thigh extension and leg coordination

- #strong[International Journal of Robotics and Automation] (2023) – Trajectory optimization of a robot arm

- #strong[Robotica] (2022) – Screw theory-based constraint wrench analysis
