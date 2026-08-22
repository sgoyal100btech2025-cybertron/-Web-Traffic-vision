/* =====================================================
   TRAFFICVISION AI ENTERPRISE ENGINE
===================================================== */

console.log(
    "%cTrafficVision AI Enterprise Loaded",
    "color:#38bdf8;font-size:18px;font-weight:bold;"
);

/* =====================================================
   GLOBAL CONFIG
===================================================== */

const TVAI = {

    version: "2.0 Enterprise",

    uploadMaxSize: 16 * 1024 * 1024,

    allowedExtensions: ["csv"],

    supportedColumns: {

        date: [
            "date",
            "day",
            "timestamp",
            "datetime",
            "time"
        ],

        visitors: [
            "visitors",
            "traffic",
            "users",
            "hits",
            "views",
            "sessions"
        ]

    }

};

/* =====================================================
   PAGE LOADER
===================================================== */

window.addEventListener("load", () => {

    const loader =
        document.querySelector(".page-loader");

    if (loader) {

        setTimeout(() => {

            loader.style.opacity = "0";

            setTimeout(() => {

                loader.style.display = "none";

            }, 600);

        }, 900);

    }

});

/* =====================================================
   ANIMATED COUNTERS
===================================================== */

function animateCounter(
    element,
    target,
    duration = 1800
) {

    let start = 0;

    const increment =
        target / (duration / 16);

    function updateCounter() {

        start += increment;

        if (start < target) {

            element.innerText =
                Math.floor(start)
                .toLocaleString();

            requestAnimationFrame(
                updateCounter
            );

        } else {

            element.innerText =
                target.toLocaleString();

        }

    }

    updateCounter();

}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document.querySelectorAll(
            ".card-value"
        ).forEach(counter => {

            const target =
                parseInt(
                    counter.innerText
                    .replace(/,/g, '')
                );

            if (!isNaN(target)) {

                counter.innerText = "0";

                animateCounter(
                    counter,
                    target
                );

            }

        });

    }
);

/* =====================================================
   LIVE CLOCK
===================================================== */

function updateClock() {

    const clock =
        document.getElementById("liveClock");

    if (clock) {

        const now = new Date();

        clock.innerHTML =
            now.toLocaleTimeString();

    }

}

setInterval(updateClock, 1000);

/* =====================================================
   TOAST NOTIFICATIONS
===================================================== */

function showToast(
    message,
    type = "success"
) {

    const toast =
        document.createElement("div");

    toast.className =
        `tv-toast ${type}`;

    const icons = {

        success:
            "bi-check-circle-fill",

        danger:
            "bi-x-circle-fill",

        warning:
            "bi-exclamation-triangle-fill",

        info:
            "bi-info-circle-fill"

    };

    toast.innerHTML = `

        <div class="toast-content">

            <i class="bi ${icons[type]}"></i>

            <span>${message}</span>

        </div>

    `;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 500);

    }, 3500);

}

/* =====================================================
   INTERSECTION ANIMATIONS
===================================================== */

const observer =
    new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add(
                    "show-animation"
                );

            }

        });

    });

document.querySelectorAll(
    ".glass-card, .prediction-card, .stat-card"
).forEach(el => {

    el.classList.add(
        "hidden-animation"
    );

    observer.observe(el);

});

/* =====================================================
   FLOATING PARTICLES
===================================================== */

function createParticle() {

    const particle =
        document.createElement("div");

    particle.className =
        "particle";

    document.body.appendChild(
        particle
    );

    const size =
        Math.random() * 5 + 2;

    particle.style.width =
        `${size}px`;

    particle.style.height =
        `${size}px`;

    particle.style.left =
        `${Math.random() * window.innerWidth}px`;

    particle.style.animationDuration =
        `${Math.random() * 8 + 5}s`;

    setTimeout(() => {

        particle.remove();

    }, 12000);

}

setInterval(createParticle, 900);

/* =====================================================
   ACTIVE MENU DETECTION
===================================================== */

const currentPath =
    window.location.pathname;

document.querySelectorAll(
    ".menu a"
).forEach(link => {

    if (
        link.getAttribute("href")
        === currentPath
    ) {

        link.classList.add("active");

    }

});

/* =====================================================
   PLOTLY CHART ANIMATION
===================================================== */

window.addEventListener("load", () => {

    const charts =
        document.querySelectorAll(
            ".js-plotly-plot"
        );

    charts.forEach(chart => {

        chart.style.opacity = "0";

        setTimeout(() => {

            chart.style.transition =
                "1s ease";

            chart.style.opacity = "1";

        }, 400);

    });

});

/* =====================================================
   RIPPLE BUTTON EFFECT
===================================================== */

document.querySelectorAll(
    ".custom-btn"
).forEach(button => {

    button.addEventListener(
        "click",
        function (e) {

            const ripple =
                document.createElement(
                    "span"
                );

            ripple.classList.add(
                "ripple"
            );

            this.appendChild(ripple);

            const x =
                e.clientX
                - e.target.offsetLeft;

            const y =
                e.clientY
                - e.target.offsetTop;

            ripple.style.left =
                `${x}px`;

            ripple.style.top =
                `${y}px`;

            setTimeout(() => {

                ripple.remove();

            }, 700);

        }
    );

});

/* =====================================================
   SCROLL TO TOP BUTTON
===================================================== */

const scrollBtn =
    document.createElement("button");

scrollBtn.innerHTML =
    '<i class="bi bi-arrow-up"></i>';

scrollBtn.className =
    "scroll-top-btn";

document.body.appendChild(
    scrollBtn
);

window.addEventListener(
    "scroll",
    () => {

        if (window.scrollY > 300) {

            scrollBtn.classList.add(
                "show-scroll"
            );

        } else {

            scrollBtn.classList.remove(
                "show-scroll"
            );

        }

    }
);

scrollBtn.addEventListener(
    "click",
    () => {

        window.scrollTo({

            top: 0,
            behavior: "smooth"

        });

    }
);

/* =====================================================
   FILE UPLOAD SYSTEM
===================================================== */

const fileInput =
    document.getElementById("fileInput");

const uploadForm =
    document.getElementById("uploadForm");

const fileName =
    document.getElementById("fileName");

const datasetPreview =
    document.getElementById("datasetPreview");

const previewFileName =
    document.getElementById("previewFileName");

const previewFileSize =
    document.getElementById("previewFileSize");

const progressContainer =
    document.getElementById("progressContainer");

const uploadProgress =
    document.getElementById("uploadProgress");

const progressPercent =
    document.getElementById("progressPercent");

const uploadLoader =
    document.getElementById("uploadLoader");

/* =====================================================
   FILE VALIDATION
===================================================== */

function validateCSV(file) {

    const extension =
        file.name
        .split('.')
        .pop()
        .toLowerCase();

    if (
        !TVAI.allowedExtensions.includes(
            extension
        )
    ) {

        showToast(
            "Only CSV files are supported!",
            "danger"
        );

        return false;

    }

    if (
        file.size >
        TVAI.uploadMaxSize
    ) {

        showToast(
            "File size exceeds 16MB limit!",
            "danger"
        );

        return false;

    }

    return true;

}

/* =====================================================
   SMART CSV ANALYZER
===================================================== */

function analyzeCSV(file) {

    const reader = new FileReader();

    reader.onload = function (e) {

        const text =
            e.target.result;

        const lines =
            text.split('\n');

        const firstLine =
            lines[0]
            .toLowerCase();

        let detectedDate = false;
        let detectedVisitors = false;

        TVAI.supportedColumns.date
            .forEach(col => {

                if (
                    firstLine.includes(col)
                ) {

                    detectedDate = true;

                }

            });

        TVAI.supportedColumns.visitors
            .forEach(col => {

                if (
                    firstLine.includes(col)
                ) {

                    detectedVisitors = true;

                }

            });

        /* Diagnostics */

        if (
            detectedDate &&
            detectedVisitors
        ) {

            showToast(
                "AI detected valid traffic dataset!",
                "success"
            );

        } else {

            showToast(
                "AI will auto-detect columns dynamically.",
                "info"
            );

        }

        /* Dataset Stats */

        const totalRows =
            Math.max(lines.length - 1, 0);

        console.log(
            `Dataset contains ${totalRows} rows`
        );

    };

    reader.readAsText(file);

}

/* =====================================================
   FILE CHANGE EVENT
===================================================== */

if (fileInput) {

    fileInput.addEventListener(
        "change",
        function () {

            if (
                this.files.length > 0
            ) {

                const file =
                    this.files[0];

                if (
                    !validateCSV(file)
                ) {

                    this.value = '';

                    return;

                }

                /* Update UI */

                if (fileName) {

                    fileName.innerHTML = `
                        <strong>${file.name}</strong>
                        selected successfully
                    `;

                }

                if (datasetPreview) {

                    datasetPreview.classList.remove(
                        "d-none"
                    );

                }

                if (previewFileName) {

                    previewFileName.innerText =
                        file.name;

                }

                if (previewFileSize) {

                    previewFileSize.innerText =
                        (
                            file.size / 1024
                        ).toFixed(2)
                        + " KB";

                }

                analyzeCSV(file);

            }

        }
    );

}

/* =====================================================
   DRAG & DROP
===================================================== */

const dropArea =
    document.getElementById("dropArea");

if (dropArea) {

    ['dragenter', 'dragover']
        .forEach(eventName => {

            dropArea.addEventListener(
                eventName,
                e => {

                    e.preventDefault();

                    dropArea.classList.add(
                        "drag-active"
                    );

                }
            );

        });

    ['dragleave', 'drop']
        .forEach(eventName => {

            dropArea.addEventListener(
                eventName,
                e => {

                    e.preventDefault();

                    dropArea.classList.remove(
                        "drag-active"
                    );

                }
            );

        });

    dropArea.addEventListener(
        "drop",
        e => {

            const files =
                e.dataTransfer.files;

            if (files.length) {

                fileInput.files = files;

                fileInput.dispatchEvent(
                    new Event("change")
                );

            }

        }
    );

}

/* =====================================================
   UPLOAD PROGRESS
===================================================== */

if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        function () {

            if (
                progressContainer
            ) {

                progressContainer.classList.remove(
                    "d-none"
                );

            }

            if (uploadLoader) {

                uploadLoader.style.display =
                    "flex";

            }

            let progress = 0;

            const interval =
                setInterval(() => {

                    progress += 4;

                    if (uploadProgress) {

                        uploadProgress.style.width =
                            progress + "%";

                    }

                    if (progressPercent) {

                        progressPercent.innerText =
                            progress + "%";

                    }

                    if (progress >= 100) {

                        clearInterval(
                            interval
                        );

                    }

                }, 100);

        }
    );

}

/* =====================================================
   CARD GLOW EFFECT
===================================================== */

document.querySelectorAll(
    ".glass-card, .prediction-card"
).forEach(card => {

    card.addEventListener(
        "mousemove",
        e => {

            const rect =
                card.getBoundingClientRect();

            const x =
                e.clientX - rect.left;

            const y =
                e.clientY - rect.top;

            card.style.setProperty(
                "--x",
                `${x}px`
            );

            card.style.setProperty(
                "--y",
                `${y}px`
            );

        }
    );

});

/* =====================================================
   PAGE TRANSITIONS
===================================================== */

document.querySelectorAll("a")
    .forEach(link => {

        link.addEventListener(
            "click",
            function () {

                if (
                    this.hostname
                    === window.location.hostname
                    &&
                    !this.hasAttribute("target")
                ) {

                    document.body.classList.add(
                        "fade-page"
                    );

                }

            }
        );

    });

/* =====================================================
   PERFORMANCE LOG
===================================================== */

console.log(
    "%cTrafficVision AI Enterprise Initialized Successfully",
    "color:#22c55e;font-size:16px;font-weight:bold;"
);