/* ================================================================
   script.js - CBSE Website Clone JavaScript
   ================================================================
   JavaScript = the BRAIN of the webpage.
   It makes the page INTERACTIVE and DYNAMIC.

   HTML  = structure (what is on the page)
   CSS   = style    (how it looks)
   JS    = behaviour (what it does when you interact)

   CONTENTS OF THIS FILE:
     1. Live Clock           -- updates time in footer every second
     2. Font Size Controls   -- A+, A, A- buttons in top bar
     3. High Contrast Mode   -- accessibility for visually impaired
     4. Search Functionality -- handles the search box
     5. Navigation           -- active link highlighting
     6. Helper function      -- focusSearch (top-right search button)

   HOW TO READ JAVASCRIPT:
     // This is a single-line comment (the browser ignores it)
     // NOTE: Multi-line comments use  slash-star ... star-slash  notation.
     //       We cannot show that here without closing THIS comment block!
     const x = 5;     // declares a constant (value cannot be changed)
     let y = 10;       // declares a variable  (value can be changed later)
     function doThing() { }  // declares a reusable block of code
================================================================ */


/* ================================================================
   STEP 1: WAIT FOR THE PAGE TO FULLY LOAD

   document.addEventListener('DOMContentLoaded', ...) waits until
   all HTML elements are parsed before running our JavaScript.

   WHY? If script tries to find an element (like #clock-display)
   before that element exists in the HTML, we get a null error.
   DOMContentLoaded ensures all elements exist first.
================================================================ */
document.addEventListener('DOMContentLoaded', function () {

  /* ============================================================
     FEATURE 1: LIVE CLOCK
     Shows the current time in the footer and updates every second.

     HOW IT WORKS:
       1. Get the <span id="clock-display"> element from HTML.
       2. Create a function that reads the current time and writes it.
       3. Run that function immediately (shows time on load).
       4. Use setInterval to run it again every 1000ms (1 second).
  ============================================================ */

  // document.getElementById('...') finds an HTML element by its id attribute.
  // We store the result in a variable so we don't have to search for it every second.
  var clockDisplay = document.getElementById('clock-display');

  // This function reads the current time and puts it in the clock element.
  function updateClock() {
    // new Date() creates an object with the current date and time
    var now = new Date();

    // Get individual time components (0-23 for hours, 0-59 for minutes/seconds)
    var hours   = now.getHours();    // e.g. 19 (for 7pm)
    var minutes = now.getMinutes();  // e.g. 35
    var seconds = now.getSeconds();  // e.g. 7

    // Determine AM or PM
    // A ternary is a short if/else: condition ? valueIfTrue : valueIfFalse
    var period = (hours >= 12) ? 'PM' : 'AM';

    // Convert from 24-hour format to 12-hour format
    hours = hours % 12; // % is the "modulo" (remainder) operator. 19 % 12 = 7
    if (hours === 0) {
      hours = 12; // midnight and noon show as 12, not 0
    }

    // padStart(2, '0') adds a leading zero if the number is only 1 digit.
    // Example: String(7).padStart(2, '0') → "07"
    // We must convert to String first because padStart is a string method.
    var hh = String(hours).padStart(2, '0');
    var mm = String(minutes).padStart(2, '0');
    var ss = String(seconds).padStart(2, '0');

    // Build the time string e.g. "07:35:07 PM"
    // Template literals use backticks (`) and ${variable} to embed values.
    var timeString = hh + ':' + mm + ':' + ss + ' ' + period;

    // .textContent sets the text content of the HTML element
    if (clockDisplay) {
      clockDisplay.textContent = timeString;
    }
  }

  // Run once immediately so the clock shows the right time on page load.
  updateClock();

  // setInterval(function, milliseconds) calls a function repeatedly.
  // 1000 ms = 1 second. So this updates the clock every second.
  setInterval(updateClock, 1000);


  /* ============================================================
     FEATURE 2: NAVIGATION — ACTIVE LINK HIGHLIGHTING
     When a nav link is clicked, it gets the 'active' CSS class
     (which makes it teal-colored). All other links lose it.
  ============================================================ */

  // querySelectorAll('.nav-link') returns ALL elements with class "nav-link"
  // as a NodeList (similar to an array).
  var navLinks = document.querySelectorAll('.nav-link');

  // .forEach loops through each item in the list and runs a function.
  navLinks.forEach(function (link) {

    // Add a 'click' event listener to each nav link.
    // When the link is clicked, the function runs.
    link.addEventListener('click', function (event) {
      // Prevent the link from navigating to '#' and scrolling to top.
      // Only do this for links that have href="#" (placeholder links).
      if (this.getAttribute('href') === '#') {
        event.preventDefault();
      }

      // Remove 'active' class from ALL nav links first.
      // This "deactivates" whichever link was active before.
      navLinks.forEach(function (l) {
        l.classList.remove('active');
      });

      // Add 'active' class to the clicked link.
      // 'this' inside an event listener refers to the clicked element.
      this.classList.add('active');
    });
  });


  /* ============================================================
     FEATURE 3: SEARCH INPUT — PRESS ENTER TO SEARCH
     Listen for the Enter key in the search box.
  ============================================================ */

  var searchInput = document.getElementById('search-input');

  if (searchInput) {
    // 'keydown' event fires whenever a key is pressed while input is focused.
    searchInput.addEventListener('keydown', function (event) {
      // event.key tells us which key was pressed.
      // 'Enter' = the Return key.
      if (event.key === 'Enter') {
        performSearch(); // Call our search function (defined below)
      }
    });
  }


  /* ============================================================
     FEATURE 4: DROPDOWN MENUS — KEYBOARD ACCESSIBILITY
     Allow keyboard users to open dropdowns with Enter/Space
     and close them with Escape.
  ============================================================ */

  // Get all nav items that have a dropdown
  var dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');

  dropdownItems.forEach(function (item) {
    var link = item.querySelector('.nav-link');
    var dropdown = item.querySelector('.dropdown-menu');

    if (!link || !dropdown) return; // Safety check

    // When link gets keyboard focus, show dropdown
    link.addEventListener('focus', function () {
      dropdown.style.display = 'block';
    });

    // When focus leaves the entire nav-item, hide dropdown
    item.addEventListener('focusout', function (event) {
      // relatedTarget = the element gaining focus
      // If focus moves outside this nav-item, close the dropdown
      if (!item.contains(event.relatedTarget)) {
        dropdown.style.display = '';  // '' resets to CSS default (which is 'none')
      }
    });

    // Close dropdown with Escape key
    item.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        dropdown.style.display = '';
        link.focus(); // Move focus back to the nav link
      }
    });
  });


  /* ============================================================
     FEATURE 9: PERSONA MARQUEE MANUAL ARROW NAVIGATION
     Clicking left (←) or right (→) buttons manual-scrolls the reel.
  ============================================================ */
  var personaWrapper = document.querySelector('.persona-marquee-wrapper');
  var personaPrevBtn = document.getElementById('personaPrevBtn');
  var personaNextBtn = document.getElementById('personaNextBtn');

  if (personaWrapper && personaPrevBtn && personaNextBtn) {
    var scrollAmount = 300; // scroll step per click (card width + gap)

    personaNextBtn.addEventListener('click', function () {
      personaWrapper.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    });

    personaPrevBtn.addEventListener('click', function () {
      personaWrapper.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    });
  }

  /* ============================================================
     FEATURE 10: STICKY NAVBAR SCROLL HANDLER
     Toggles .is-sticky class on scroll down to trigger shadow & blur
  ============================================================ */
  var mainNav = document.querySelector('.main-nav');
  if (mainNav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 80) {
        mainNav.classList.add('is-sticky');
      } else {
        mainNav.classList.remove('is-sticky');
      }
    });
  }


  /* ============================================================
     FEATURE 11: CBSE AI ASSISTANT CHATBOT INTERACTIVES
  ============================================================ */
  var cbseWidget = document.getElementById('cbseChatbotWidget');
  var chatbotTriggerBtn = document.getElementById('chatbotTriggerBtn');
  var chatbotCloseBtn = document.getElementById('chatbotCloseBtn');
  var chatbotSendBtn = document.getElementById('chatbotSendBtn');
  var chatbotInput = document.getElementById('chatbotInput');
  var chatbotBody = document.getElementById('chatbotBody');

  if (cbseWidget && chatbotTriggerBtn && chatbotCloseBtn) {
    // Toggle chatbot open/close
    chatbotTriggerBtn.addEventListener('click', function () {
      cbseWidget.classList.toggle('active');
      if (cbseWidget.classList.contains('active') && chatbotInput) {
        chatbotInput.focus();
      }
    });

    chatbotCloseBtn.addEventListener('click', function () {
      cbseWidget.classList.remove('active');
    });

    // Send message handlers
    if (chatbotSendBtn && chatbotInput) {
      chatbotSendBtn.addEventListener('click', handleUserSendMessage);
      chatbotInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          handleUserSendMessage();
        }
      });
    }
  }

  function handleUserSendMessage() {
    if (!chatbotInput) return;
    var text = chatbotInput.value.trim();
    if (text === '') return;

    addUserChatMessage(text);
    chatbotInput.value = '';
    processBotResponse(text);
  }

  function addUserChatMessage(msgText) {
    if (!chatbotBody) return;
    var userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message user-message';
    userMsgDiv.innerHTML = '<div class="message-content"><p>' + escapeHtml(msgText) + '</p></div>';
    chatbotBody.appendChild(userMsgDiv);
    chatbotBody.scrollTop = chatbotBody.scrollHeight;
  }

  function processBotResponse(userMsg) {
    if (!chatbotBody) return;

    // Show typing indicator
    var typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message typing-msg';
    typingDiv.innerHTML = '<div class="message-content typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>';
    chatbotBody.appendChild(typingDiv);
    chatbotBody.scrollTop = chatbotBody.scrollHeight;

    setTimeout(function () {
      typingDiv.remove();
      var botReply = generateBotReply(userMsg);
      var botMsgDiv = document.createElement('div');
      botMsgDiv.className = 'chat-message bot-message';
      botMsgDiv.innerHTML = '<div class="message-content">' + botReply + '</div>';
      chatbotBody.appendChild(botMsgDiv);
      chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }, 1000);
  }

  function generateBotReply(query) {
    var lower = query.toLowerCase();
    if (lower.includes('result') || lower.includes('marks')) {
      return '<p>You can check the latest Class X & XII Board Exam Results on the official <strong>Parinam Manjusha</strong> portal or DigiLocker.</p><p>👉 Visit <a href="https://results.cbse.nic.in" target="_blank" style="color:#2ea2c7; text-decoration:underline;">results.cbse.nic.in</a></p>';
    } else if (lower.includes('ctet')) {
      return '<p>CTET 2026 notifications, eligibility criteria, and application forms are available on the official CTET portal.</p><p>👉 Visit <a href="https://ctet.nic.in" target="_blank" style="color:#2ea2c7; text-decoration:underline;">ctet.nic.in</a></p>';
    } else if (lower.includes('admit') || lower.includes('hall ticket')) {
      return '<p>Admit Cards for private candidates and regular schools can be downloaded directly from the <strong>Main CBSE Portal</strong>.</p>';
    } else if (lower.includes('verif') || lower.includes('reval')) {
      return '<p>Online applications for Verification of Marks & Re-evaluation are processed under the <strong>Verification Process Portal</strong>.</p>';
    } else if (lower.includes('hello') || lower.includes('hi') || lower.includes('hey')) {
      return '<p>Hello! How can I help you today? Feel free to ask about results, admit cards, or circulars!</p>';
    } else {
      return '<p>Thank you for reaching out! For official queries, please refer to the main CBSE circulars or call the toll-free helpline <strong>1800-11-8002</strong>.</p>';
    }
  }

  // Global function for quick chip buttons
  window.sendQuickMessage = function (text) {
    if (cbseWidget && !cbseWidget.classList.contains('active')) {
      cbseWidget.classList.add('active');
    }
    addUserChatMessage(text);
    processBotResponse(text);
  };

}); // End of DOMContentLoaded


/* ================================================================
   FEATURE 5: FONT SIZE CONTROLS
   These functions are called from HTML onclick attributes:
     onclick="changeFontSize('increase')"
     onclick="changeFontSize('normal')"
     onclick="changeFontSize('decrease')"

   They add a CSS class to <body> which changes font size.
   The CSS classes (.font-large, .font-small) are defined in styles.css.
================================================================ */

// changeFontSize is a GLOBAL function (outside DOMContentLoaded)
// so it can be called directly from onclick="" in HTML.
function changeFontSize(action) {
  // document.body = the <body> element
  // classList = the list of CSS classes on the element

  // First, remove any existing font-size class
  document.body.classList.remove('font-large', 'font-small');

  // Then add the appropriate class
  if (action === 'increase') {
    document.body.classList.add('font-large');
  } else if (action === 'decrease') {
    document.body.classList.add('font-small');
  }
  // If action === 'normal', we already removed classes — that's all we need.
}


/* ================================================================
   FEATURE 6: HIGH CONTRAST MODE
   Toggles a CSS class on <body> that inverts colors for accessibility.
   Called from: onclick="toggleHighContrast()" in HTML.
================================================================ */
function toggleHighContrast() {
  // classList.toggle() adds the class if it's not there, removes it if it is.
  // It's like a light switch — toggle on/off.
  document.body.classList.toggle('high-contrast');

  // Update the contrast button's visual state
  var contrastBtn = document.getElementById('contrast-btn');
  if (contrastBtn) {
    // classList.contains() checks if a class is present (returns true/false)
    if (document.body.classList.contains('high-contrast')) {
      // Active: show teal background to indicate it's on
      contrastBtn.classList.add('active-contrast');
      // Update accessible title text
      contrastBtn.title = 'Turn off high contrast mode';
    } else {
      contrastBtn.classList.remove('active-contrast');
      contrastBtn.title = 'Toggle high contrast mode';
    }
  }
}


/* ================================================================
   FEATURE 7: SEARCH FUNCTIONALITY
   Handles what happens when the user clicks Search or presses Enter.
   Called from: onclick="performSearch()" in HTML (button) and
                event listener above (Enter key).
================================================================ */
function performSearch() {
  // Get the search input element and read its current value
  var searchInput = document.getElementById('search-input');
  var resultsArea = document.getElementById('search-results-area');

  // Safety check: if elements don't exist, stop here
  if (!searchInput || !resultsArea) return;

  // .value reads what the user typed
  // .trim() removes any leading/trailing spaces
  //   Example: "  hello world  " → "hello world"
  var query = searchInput.value.trim();

  // If the user typed nothing, show a helpful message
  if (query === '') {
    resultsArea.innerHTML = '<p style="color:#e74c3c; font-size:13px;">⚠ Please enter a search term first.</p>';
    searchInput.focus(); // Put cursor back in the input box
    return; // Stop the function here (don't continue)
  }

  // Show a "searching..." feedback message while navigating
  // innerHTML lets us set HTML content (not just plain text)
  resultsArea.innerHTML = '<p style="color:#555; font-size:13px;">🔍 Searching for: <strong>' + escapeHtml(query) + '</strong>...</p>';

  // Open Google Search filtered to the CBSE website in a new browser tab.
  // encodeURIComponent() makes the query safe for a URL.
  // Example: "board exam 2026" → "board%20exam%202026"
  var searchUrl = 'https://www.google.com/search?q=site:cbse.gov.in+' + encodeURIComponent(query);

  // window.open(url, '_blank') opens the URL in a new tab
  window.open(searchUrl, '_blank');
}


/* ================================================================
   HELPER: FOCUS THE SEARCH INPUT
   Called when the top-right search button (magnifying glass) is clicked.
   Scrolls to the search section and puts the cursor in the input box.
================================================================ */
function focusSearch() {
  // document.getElementById finds the element
  var searchInput = document.getElementById('search-input');
  var mainContent = document.getElementById('main-content');

  if (mainContent) {
    // scrollIntoView smoothly scrolls the element into the visible area
    mainContent.scrollIntoView({ behavior: 'smooth' });
  }

  if (searchInput) {
    // setTimeout waits a short time before focusing (so scroll finishes first)
    // The first argument is the function to run, second is delay in milliseconds
    setTimeout(function () {
      searchInput.focus(); // .focus() places the text cursor inside the input
    }, 400);
  }
}


/* ================================================================
   SECURITY HELPER: ESCAPE HTML
   When displaying user-typed text in .innerHTML, we must escape
   special characters to prevent Cross-Site Scripting (XSS) attacks.

   Example: if user types: <script>alert('hacked')</script>
   Without escaping: the browser would RUN that script!
   With escaping: it shows: &lt;script&gt;alert('hacked')&lt;/script&gt;

   This is an important security practice even for simple pages.
================================================================ */
function escapeHtml(text) {
  // Create a temporary div element
  var div = document.createElement('div');
  // Set its text content (this automatically escapes special characters)
  div.appendChild(document.createTextNode(text));
  // Return the escaped HTML
  return div.innerHTML;
}


/* ================================================================
   FEATURE 8: HERO BANNER CAROUSEL SLIDER
   Allows switching hero slides using next/prev buttons and dots.
================================================================ */
var currentSlideIndex = 0;
var slideData = [
  {
    image: 'https://www.cbse.gov.in/cbsenew/images/Cyber_crime.JPG',
    link: 'https://cybercrime.gov.in/',
    title: 'Cyber Crime Reporting Portal'
  },
  {
    image: 'https://www.cbse.gov.in/cbsenew/images/ncw_banner.jpg',
    link: 'https://www.ncwwomenhelpline.in',
    title: 'NCW Women Helpline'
  },
  {
    image: 'https://www.cbse.gov.in/cbsenew/images/header/SAFAL%20Banner%20.jpg',
    link: 'https://www.cbse.gov.in/cbsenew/documents//safal_video.mp4',
    title: 'SAFAL Assessment Framework'
  },
  {
    image: 'https://www.cbse.gov.in/cbsenew/images/banner_Main_08052025.jpg',
    link: '#',
    title: 'CBSE Academic Initiatives'
  }
];

function updateSlideUI() {
  var track = document.getElementById('heroSliderTrack');
  var dotsContainer = document.querySelector('.carousel-dots');

  if (track) {
    var translateXPercent = -(currentSlideIndex * 25); // 25% width per slide (4 slides)
    track.style.transform = 'translateX(' + translateXPercent + '%)';
  }

  if (dotsContainer) {
    var dotsHtml = '';
    for (var i = 0; i < slideData.length; i++) {
      dotsHtml += '<span class="dot ' + (i === currentSlideIndex ? 'active' : '') + '" onclick="setSlide(' + i + ')"></span>';
    }
    dotsContainer.innerHTML = dotsHtml;
  }
}

/* Auto-scroll timer for Hero Carousel */
var heroAutoTimer = null;

function startHeroAutoScroll() {
  stopHeroAutoScroll();
  heroAutoTimer = setInterval(function () {
    nextSlide();
  }, 4000);
}

function stopHeroAutoScroll() {
  if (heroAutoTimer) {
    clearInterval(heroAutoTimer);
    heroAutoTimer = null;
  }
}

function setSlide(index) {
  currentSlideIndex = index;
  updateSlideUI();
  startHeroAutoScroll();
}

function nextSlide() {
  currentSlideIndex = (currentSlideIndex + 1) % slideData.length;
  updateSlideUI();
}

function prevSlide() {
  currentSlideIndex = (currentSlideIndex - 1 + slideData.length) % slideData.length;
  updateSlideUI();
  startHeroAutoScroll();
}

// Start auto-scroll on page load
startHeroAutoScroll();

// Pause auto-scroll when hovering over the hero card
var heroCardElem = document.getElementById('heroCard');
if (heroCardElem) {
  heroCardElem.addEventListener('mouseenter', stopHeroAutoScroll);
  heroCardElem.addEventListener('mouseleave', startHeroAutoScroll);
}


/* ================================================================
   PORTAL SEARCH & AI SEMANTIC SEARCH CONTROLLER
   Integrates with Python FastAPI Backend Endpoint (/api/search)
================================================================ */

var currentSearchResults = [];
var activeFilterTab = 'all';

// Initialize search event listeners on input change, shortcut & autocomplete
var autocompleteTimer = null;

document.addEventListener('DOMContentLoaded', function () {
  var searchInput = document.getElementById('search-input');
  var clearBtn = document.getElementById('search-clear-btn');
  var autocompleteDropdown = document.getElementById('search-autocomplete-dropdown');

  // Global Keyboard Shortcut: Ctrl+K or Cmd+K to focus search input
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
        var searchSection = document.getElementById('portal-search-section');
        if (searchSection) {
          searchSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    }
  });
  
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      var query = searchInput.value.trim();
      if (clearBtn) {
        clearBtn.style.display = query ? 'flex' : 'none';
      }

      // Debounced live autocomplete
      clearTimeout(autocompleteTimer);
      if (query.length >= 2) {
        autocompleteTimer = setTimeout(function () {
          fetchAutocompleteSuggestions(query);
        }, 220);
      } else {
        hideAutocompleteDropdown();
      }
    });

    // Pressing Escape clears search & hides dropdown
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        clearSearchInput();
        hideAutocompleteDropdown();
      }
    });

    // Close autocomplete dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!e.target.closest('#portal-search-form')) {
        hideAutocompleteDropdown();
      }
    });
  }
});

function hideAutocompleteDropdown() {
  var dropdown = document.getElementById('search-autocomplete-dropdown');
  if (dropdown) {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
  }
}

async function fetchAutocompleteSuggestions(query) {
  var dropdown = document.getElementById('search-autocomplete-dropdown');
  var toggleCheckbox = document.getElementById('semantic-toggle-checkbox');
  if (!dropdown) return;

  try {
    var isSemantic = toggleCheckbox ? toggleCheckbox.checked : true;
    var res = await fetch('/api/search?q=' + encodeURIComponent(query) + '&semantic=' + (isSemantic ? 'true' : 'false'));
    if (!res.ok) return;

    var data = await res.json();
    var matches = (data.results || []).slice(0, 4);

    if (matches.length === 0) {
      hideAutocompleteDropdown();
      return;
    }

    var html = matches.map(function (item) {
      var icon = item.type === 'service' ? 'fa-concierge-bell' : (item.type === 'news' ? 'fa-newspaper' : 'fa-file-pdf');
      var typeColor = item.type === 'service' ? 'color-service' : (item.type === 'news' ? 'color-news' : 'color-circular');
      return `
        <div class="autocomplete-item" onclick="selectAutocompleteItem('${escapeHtml(item.title).replace(/'/g, "\\'")}')">
          <i class="fas ${icon} ${typeColor}"></i>
          <div class="autocomplete-info">
            <span class="autocomplete-title">${escapeHtml(item.title)}</span>
            <span class="autocomplete-meta">${escapeHtml(item.category || 'General')} &bull; ${escapeHtml(item.date || '')}</span>
          </div>
          <i class="fas fa-arrow-right autocomplete-arrow"></i>
        </div>
      `;
    }).join('');

    dropdown.innerHTML = `
      <div class="autocomplete-header">
        <span><i class="fas fa-sparkles"></i> Live Suggestions for "${escapeHtml(query)}"</span>
      </div>
      <div class="autocomplete-list">${html}</div>
    `;
    dropdown.style.display = 'block';
  } catch (err) {
    console.debug('Autocomplete fetch ignored:', err);
  }
}

function selectAutocompleteItem(title) {
  var searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.value = title;
  }
  hideAutocompleteDropdown();
  handleSearchSubmit();
}

function clearSearchInput() {
  var searchInput = document.getElementById('search-input');
  var clearBtn = document.getElementById('search-clear-btn');
  var resultsPanel = document.getElementById('search-results-panel');
  if (searchInput) {
    searchInput.value = '';
    searchInput.focus();
  }
  if (clearBtn) {
    clearBtn.style.display = 'none';
  }
  if (resultsPanel) {
    resultsPanel.style.display = 'none';
  }
  hideAutocompleteDropdown();
  currentSearchResults = [];
}

function handleSemanticToggleChange(event) {
  var isChecked = event.target.checked;
  var modeHint = document.getElementById('search-mode-hint');
  if (modeHint) {
    if (isChecked) {
      modeHint.innerHTML = '<i class="fas fa-brain toggle-ai-icon"></i> AI Semantic Mode matches concepts &amp; context using vector similarity';
      modeHint.classList.add('ai-active-hint');
    } else {
      modeHint.innerHTML = '<i class="fas fa-filter"></i> Keyword Mode matches exact text terms in title &amp; description';
      modeHint.classList.remove('ai-active-hint');
    }
  }

  // Re-run search if query exists
  var searchInput = document.getElementById('search-input');
  if (searchInput && searchInput.value.trim().length >= 2) {
    executePortalSearch(searchInput.value.trim(), isChecked);
  }
}

function handleSearchSubmit(event) {
  if (event) event.preventDefault();
  hideAutocompleteDropdown();

  var searchInput = document.getElementById('search-input');
  var toggleCheckbox = document.getElementById('semantic-toggle-checkbox');
  
  if (!searchInput) return;
  var query = searchInput.value.trim();
  
  if (!query) {
    searchInput.focus();
    return;
  }
  
  var isSemantic = toggleCheckbox ? toggleCheckbox.checked : true;
  executePortalSearch(query, isSemantic);
}

function quickSearch(queryText) {
  hideAutocompleteDropdown();
  var searchInput = document.getElementById('search-input');
  var clearBtn = document.getElementById('search-clear-btn');
  var toggleCheckbox = document.getElementById('semantic-toggle-checkbox');
  
  if (searchInput) {
    searchInput.value = queryText;
    if (clearBtn) clearBtn.style.display = 'flex';
  }
  
  var isSemantic = toggleCheckbox ? toggleCheckbox.checked : true;
  executePortalSearch(queryText, isSemantic);
  
  // Scroll smoothly to search section if needed
  var searchSection = document.getElementById('portal-search-section');
  if (searchSection) {
    searchSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

async function executePortalSearch(query, isSemantic) {
  var panel = document.getElementById('search-results-panel');
  var loader = document.getElementById('search-skeleton-loader');
  var resultsList = document.getElementById('search-results-list');
  var emptyState = document.getElementById('search-empty-state');
  var countTitle = document.getElementById('results-count-title');
  var queryBadge = document.getElementById('results-query-badge');

  if (!panel || !resultsList) return;

  // Show panel, show loader, hide list & empty state
  panel.style.display = 'block';
  if (loader) loader.style.display = 'grid';
  if (resultsList) resultsList.style.display = 'none';
  if (emptyState) emptyState.style.display = 'none';

  if (queryBadge) {
    queryBadge.innerHTML = 'Query: <strong>"' + escapeHtml(query) + '"</strong> ' + 
      (isSemantic ? '<span class="badge-tag-ai"><i class="fas fa-sparkles"></i> AI Semantic</span>' : '<span class="badge-tag-keyword"><i class="fas fa-font"></i> Keyword</span>');
  }

  try {
    var apiUrl = '/api/search?q=' + encodeURIComponent(query) + '&semantic=' + (isSemantic ? 'true' : 'false');
    var response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error('Search failed with status ' + response.status);
    }

    var data = await response.json();
    currentSearchResults = data.results || [];

    if (loader) loader.style.display = 'none';

    if (countTitle) {
      countTitle.textContent = 'Found ' + currentSearchResults.length + ' Result' + (currentSearchResults.length === 1 ? '' : 's');
    }

    if (currentSearchResults.length === 0) {
      if (emptyState) emptyState.style.display = 'flex';
      return;
    }

    if (resultsList) {
      resultsList.style.display = 'grid';
      renderSearchResults(activeFilterTab);
    }
  } catch (error) {
    console.error('Portal Search Error:', error);
    if (loader) loader.style.display = 'none';
    if (emptyState) {
      emptyState.style.display = 'flex';
      emptyState.querySelector('h4').textContent = 'Unable to fetch results';
      emptyState.querySelector('p').textContent = 'Please make sure the backend Python server is running and try again.';
    }
  }
}

function filterSearchResults(filterType) {
  activeFilterTab = filterType;
  
  // Update active tab UI
  var tabBtns = document.querySelectorAll('.results-filter-tabs .tab-btn');
  tabBtns.forEach(function (btn) {
    if (btn.getAttribute('data-filter') === filterType) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  renderSearchResults(filterType);
}

function renderSearchResults(filterType) {
  var resultsList = document.getElementById('search-results-list');
  var emptyState = document.getElementById('search-empty-state');
  if (!resultsList) return;

  var filtered = currentSearchResults;
  if (filterType !== 'all') {
    filtered = currentSearchResults.filter(function (item) {
      return item.type === filterType;
    });
  }

  if (filtered.length === 0) {
    resultsList.style.display = 'none';
    if (emptyState) {
      emptyState.style.display = 'flex';
      emptyState.querySelector('h4').textContent = 'No ' + filterType + ' results found';
      emptyState.querySelector('p').textContent = 'Try selecting "All Results" or enabling AI Semantic Search.';
    }
    return;
  }

  if (emptyState) emptyState.style.display = 'none';
  resultsList.style.display = 'grid';

  var cardsHtml = filtered.map(function (item) {
    var matchBadge = item.match_type === 'semantic' 
      ? '<span class="match-badge badge-semantic"><i class="fas fa-brain"></i> AI Semantic Match</span>'
      : '<span class="match-badge badge-keyword"><i class="fas fa-magnifying-glass"></i> Keyword Match</span>';
      
    var scorePct = (item.similarity_score !== null && item.similarity_score !== undefined) ? Math.round(item.similarity_score * 100) : null;
    var similarityBadge = (scorePct !== null)
      ? `
        <div class="score-pill-group" title="Vector similarity score: ${scorePct}%">
          <span class="score-badge"><i class="fas fa-chart-line"></i> ${scorePct}% Relevance</span>
          <div class="score-bar-track"><div class="score-bar-fill" style="width: ${Math.min(Math.max(scorePct, 10), 100)}%;"></div></div>
        </div>
      `
      : '';

    var typeClass = 'type-' + (item.type || 'circular');
    var typeLabel = item.type ? item.type.toUpperCase() : 'CIRCULAR';
    var iconClass = item.type === 'service' ? 'fa-concierge-bell' : (item.type === 'news' ? 'fa-newspaper' : 'fa-file-pdf');

    var linkUrl = item.document_url || item.source_url || '#';
    var hasDirectLink = linkUrl && linkUrl !== '#';

    return `
      <div class="search-result-card ${typeClass}">
        <div class="result-card-header">
          <div class="result-badges-row">
            <span class="type-pill ${typeClass}"><i class="fas ${iconClass}"></i> ${typeLabel}</span>
            <span class="category-pill">${escapeHtml(item.category || 'General')}</span>
            ${matchBadge}
            ${similarityBadge}
          </div>
          <span class="result-date"><i class="far fa-calendar-alt"></i> ${escapeHtml(item.date || '')}</span>
        </div>

        <h4 class="result-card-title">
          <a href="${escapeHtml(linkUrl)}" ${hasDirectLink ? 'target="_blank" rel="noopener"' : ''}>
            ${escapeHtml(item.title)}
          </a>
        </h4>

        <p class="result-card-description">
          ${escapeHtml(item.description || 'Official CBSE document notification.')}
        </p>

        <div class="result-card-footer">
          <a href="${escapeHtml(linkUrl)}" ${hasDirectLink ? 'target="_blank" rel="noopener"' : ''} class="result-action-btn">
            ${item.document_url ? '<i class="fas fa-download"></i> View / Download Document' : '<i class="fas fa-external-link-alt"></i> Access Portal Link'}
          </a>
        </div>
      </div>
    `;
  }).join('');

  resultsList.innerHTML = cardsHtml;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}








