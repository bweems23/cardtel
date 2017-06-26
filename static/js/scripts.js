
window.onscroll = function() { handleScrollEvents() };



function handleScrollEvents() {
  scrollPosition = document.body.scrollTop;

  var navigation = document.getElementById("navigation");

  if (scrollPosition < 320) {
    var newPosition = (380 - scrollPosition) + "px";
    navigation.style.marginTop = newPosition;
  } else {
    navigation.style.marginTop = "60px";
  }

  var sections = ['intro', 'rules', 'practices', 'history', 'twitter'];

  var selectedSection;
  for (i = 0; i < sections.length; i++) {
      currentSection = sections[i];
      var section = document.getElementById(currentSection);
      var position = section.getBoundingClientRect().top;
      if (i == 0 && position > 0) { 
        selectedSection = currentSection;
        break;
      }
      if (position > -60) {
        if (position > 120) { 
          selectedSection = sections[i - 1];
        } else {
          selectedSection = currentSection;
        }
        break;
      }
      if (i == sections.length) {
        selectedSection = sections[sections.length - 1];
        break;
      }
  }

  for (i = 0; i < sections.length; i++) {
    var selectedID = "nav-" + sections[i];
    var selectedElement = document.getElementById(selectedID);
    if (sections[i] == selectedSection) {
      selectedElement.classList.add("selected");
      console.log(selectedElement)

    } else {
      selectedElement.classList.remove("selected");
    }
  }

}






var EPPZScrollTo =
{
    /**
     * Helpers.
     */
    documentVerticalScrollPosition: function()
    {
        if (self.pageYOffset) return self.pageYOffset; // Firefox, Chrome, Opera, Safari.
        if (document.documentElement && document.documentElement.scrollTop) return document.documentElement.scrollTop; // Internet Explorer 6 (standards mode).
        if (document.body.scrollTop) return document.body.scrollTop; // Internet Explorer 6, 7 and 8.
        return 0; // None of the above.
    },

    viewportHeight: function()
    { return (document.compatMode === "CSS1Compat") ? document.documentElement.clientHeight : document.body.clientHeight; },

    documentHeight: function()
    { return (document.height !== undefined) ? document.height : document.body.offsetHeight; },

    documentMaximumScrollPosition: function()
    { return this.documentHeight() - this.viewportHeight(); },

    elementVerticalClientPositionById: function(id)
    {
        var element = document.getElementById(id);
        var rectangle = element.getBoundingClientRect();
        return rectangle.top;
    },

    /**
     * Animation tick.
     */
    scrollVerticalTickToPosition: function(currentPosition, targetPosition)
    {
        var filter = 0.2;
        var fps = 60;
        var difference = parseFloat(targetPosition) - parseFloat(currentPosition);

        // Snap, then stop if arrived.
        var arrived = (Math.abs(difference) <= 0.5);
        if (arrived)
        {
            // Apply target.
            scrollTo(0.0, targetPosition);
            return;
        }

        // Filtered position.
        currentPosition = (parseFloat(currentPosition) * (1.0 - filter)) + (parseFloat(targetPosition) * filter);

        // Apply target.
        scrollTo(0.0, Math.round(currentPosition));

        // Schedule next tick.
        setTimeout("EPPZScrollTo.scrollVerticalTickToPosition("+currentPosition+", "+targetPosition+")", (1000 / fps));
    },

    /**
     * For public use.
     *
     * @param id The id of the element to scroll to.
     * @param padding Top padding to apply above element.
     */
    scrollVerticalToElementById: function(id, padding)
    {
        var element = document.getElementById(id);
        if (element == null)
        {
            console.warn('Cannot find element with id \''+id+'\'.');
            return;
        }

        var targetPosition = this.documentVerticalScrollPosition() + this.elementVerticalClientPositionById(id) - padding;
        var currentPosition = this.documentVerticalScrollPosition();

        // Clamp.
        var maximumScrollPosition = this.documentMaximumScrollPosition();
        if (targetPosition > maximumScrollPosition) targetPosition = maximumScrollPosition;

        // Start animation.
        this.scrollVerticalTickToPosition(currentPosition, targetPosition);
    }

};



function navigate(id, object) {
  EPPZScrollTo.scrollVerticalToElementById(id, 20);
}
