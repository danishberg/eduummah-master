import React from 'react';

function Welcome() {
  const Carousel = ({ carouselItems, ...rest }) => {
    const [active, setActive] = React.useState(0);
    let scrollInterval = null;

    React.useEffect(() => {
      scrollInterval = setTimeout(() => {
        setActive((active + 1) % carouselItems.length);
      }, 2000);
      return () => clearTimeout(scrollInterval);
    });

    return (
      <div className="carousel">
        {carouselItems.map((item, index) => {
          const activeClass = active === index ? ' visible' : '';
          return React.cloneElement(item, {
            ...rest,
            className: `carousel-item${activeClass}`
          });
        })}
      </div>
    );
  };

  return (
    <div className="Welcome">
      <h2>Welcome page</h2>
      <p>Welcome to the Welcome page of EduUmmah!</p>
      {/* Including the Carousel component */}
      <Carousel
        carouselItems={[
          <div>carousel item 1</div>,
          <div>carousel item 2</div>,
          <div>carousel item 3</div>
        ]}
      />
      {/* Add more content or components as needed */}
    </div>
  );
}

export default Welcome;
