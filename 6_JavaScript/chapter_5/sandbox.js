// Object literal notation -> {}

let user = {
    // Properties
    name: 'john',
    age: 36,
    email: 'john@example.com',
    location: 'Aukland',
    blogs: ['Why Kiwis rule rugny!', 'But did you die?'],

    // Mehods
    login(){
        console.log('User logged in');
    },
    logout: function(){
        console.log('User logged out');
    },
    logBlogs(){
        console.log('This user has written the following blogs:');
        this.blogs.forEach(blog => {
            console.log(blog);
        });
    }
};

user.login();
user.logout();
user.logBlogs();