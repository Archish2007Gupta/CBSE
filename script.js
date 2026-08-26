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
    title: 'Examinations<br>2026',
    subtitle: 'Latest updates, notifications, date sheets, results and more.',
    btnText: 'View All Updates'
  },
  {
    title: 'Academic<br>Resources',
    subtitle: 'Curriculum frameworks, sample question papers and learning materials.',
    btnText: 'Explore Academics'
  },
  {
    title: 'Digital<br>Services',
    subtitle: 'Access DigiLocker certificates, online verification, and student portals.',
    btnText: 'Access Services'
  }
];

function updateSlideUI() {
  var titleEl = document.getElementById('hero-title');
  var subEl   = document.getElementById('hero-subtitle');
  var btnEl   = document.getElementById('hero-btn');
  var dots    = document.querySelectorAll('.carousel-dots .dot');

  if (titleEl && slideData[currentSlideIndex]) {
    titleEl.innerHTML = slideData[currentSlideIndex].title;
    subEl.textContent = slideData[currentSlideIndex].subtitle;
    btnEl.textContent = slideData[currentSlideIndex].btnText;
  }

  dots.forEach(function (dot, idx) {
    if (idx === currentSlideIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
}

function setSlide(index) {
  currentSlideIndex = index;
  updateSlideUI();
}

function nextSlide() {
  currentSlideIndex = (currentSlideIndex + 1) % slideData.length;
  updateSlideUI();
}

function prevSlide() {
  currentSlideIndex = (currentSlideIndex - 1 + slideData.length) % slideData.length;
  updateSlideUI();
}

