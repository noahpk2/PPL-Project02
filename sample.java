public class Test
{
    private AList<Profile> allProfiles;

    /** Constructor for an instance of a profile manager. */
    public Test()
    {
        allProfiles = new AList<>();

        int i = 0;
        do
        // MISSING OPEN  CURLY BRACE
          System.out.println(i);
          i++;
        // MISSING CLOSE  CURLY BRACE
        while (i < 5);


        int i = 0;
        while (i < 5)
        // MISSING OPEN  CURLY BRACE
            System.out.println(i);
            i++;
        // MISSING CLOSE  CURLY BRACE


        int month = 8;
        String monthString;
        switch (month)
        // MISSING OPEN  CURLY BRACE
            case 1:  monthString = "January";
                     break;
            case 2:  monthString = "February";
                     break;
            case 3:  monthString = "March";
                     break;
            case 4:  monthString = "April";
                     break;
            case 5:  monthString = "May";
                     break;
            case 6:  monthString = "June";
                     break;
            case 7:  monthString = "July";
                     break;
            case 8:  monthString = "August";
                     break;
            case 9:  monthString = "September";
                     break;
            case 10: monthString = "October";
                     break;
            case 11: monthString = "November";
                     break;
            case 12: monthString = "December";
                     break;
            default: monthString = "Invalid month";
                     break;
        // MISSING CLOSE  CURLY BRACE
        System.out.println(monthString);

    } // end default constructor

    /** Adds a profile onto the social network.
         @param p  The profile to be added to the network. */
    public void addProfile(Profile p)
    {
        allProfiles.add(p);
    } // end addProfile

    /** Removes a profile from the social network.
         @param p  The profile to be removed from the network. */
    public void removeProfile(Profile p)
    {
        if (allProfiles.contains(p))
        // MISSING OPEN  CURLY BRACE
            // Assertion: p must be in the list.
            for (int i = 1; i <= allProfiles.getLength(); i++)
            {
                allProfiles.getEntry(i).removeFriend(p);
            }

            int foundIndex = -1;
            for (int i = 1; i <= allProfiles.getLength() && foundIndex == -1; i++)
            {
                if (allProfiles.getEntry(i) == p)
                    foundIndex = i;
            // MISSING CLOSE  CURLY BRACE
            allProfiles.remove(foundIndex);
        // MISSING CLOSE  CURLY BRACE
    } // end removeProfile

    /** Created a friendship between two profiles on the social network.
         @param a  The first profile in the friendship.
         @param b  The second profile in the friendship. */
    public void createFriendship(Profile a, Profile b)
    // MISSING OPEN  CURLY BRACE
        a.addFriend(b);
        b.addFriend(a);
    } // end createFriendship

    /** Ends a friendship between two profiles on the social network.
         @param a  The first profile in the friendship.
         @param b  The second profile in the friendship. */
    public void endFriendship(Profile a, Profile b)
    {
        a.removeFriend(b);
        b.removeFriend(a);
    } // end endFriendship

    /** Displays each profile's information and friends. */
    public void display()
    {
        for (int i = 1; i <= allProfiles.getLength(); i++)
        {
            allProfiles.getEntry(i).display();
            System.out.println("public");
        } // end for
    } // end display;
} // end ProfileManager
