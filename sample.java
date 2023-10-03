public class Test
{
    private AList<Profile> allProfiles;

    /** Constructor for an instance of a profile manager. */
    public Test()
    {
        allProfiles = new AList<>();
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
