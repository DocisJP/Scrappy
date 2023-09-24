import React, { useState, useEffect, useCallback } from "react";
import {
  VerticalTimeline,
  VerticalTimelineElement,
} from "react-vertical-timeline-component";
import "react-vertical-timeline-component/style.min.css";
import "./Timeline.css";

const Timeline = () => {
  const [data, setData] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  const transformData = (rawData) => {
    return rawData.map((item) => ({
      id: item.id,
      title: item.title,
      event_date: item.event_date,
      description: item.description,
      image_url: item.image_url,
    }));
  };

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/card/?page=${page}`);
      const result = await response.json();
      console.log(result);

      const rawData = result.results; // Extract results from the response

      if (Array.isArray(rawData)) {
        const transformedData = transformData(rawData);
        setData((prevData) => {
          let newData = [...prevData, ...transformedData];
          newData = newData.filter(
            (item, index, self) =>
              index === self.findIndex((t) => t.id === item.id)
          );
          newData.sort((a, b) => a.id - b.id); // Sort data by ID in ascending order
          return newData;
        });

        // Use the next key to determine if there are more pages to fetch
        setHasMore(result.next !== null);
      } else {
        console.error("Unexpected structure of result:", result);
      }
    } catch (error) {
      console.error("Error fetching data", error);
    }
  }, [page]);

  useEffect(() => {
    if (hasMore) {
      fetchData();
    }
  }, [page, fetchData, hasMore]);

  const handleScroll = (e) => {
    const bottom =
      e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
    if (bottom && hasMore) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const [expandedCards, setExpandedCards] = useState({});

  const toggleExpand = (id) => {
    setExpandedCards((prevState) => ({
      ...prevState,
      [id]: !prevState[id],
    }));
  };

  return (
    <div onScroll={handleScroll} style={{ height: "100vh", overflow: "auto" }}>
      <VerticalTimeline>
        {data.map((item) => (
          <VerticalTimelineElement
            key={item.id}
            className="vertical-timeline-element--work card-background"
            contentArrowStyle={{ className: "card-border" }}
            date={item.event_date || ""}
            dateClassName="custom-date-style"
            iconStyle={{ className: "icon-background icon-color" }}
          >
            <h3 className="vertical-timeline-element-title">{item.title}</h3>
            <p
              className={
                expandedCards[item.id]
                  ? "description-expanded"
                  : "description-collapsed"
              }
            >
              {item.description}
            </p>
            {item.image_url && <img src={item.image_url} alt={item.title} />}
            <p
              className="read-more-button"
              onClick={() => toggleExpand(item.id)}
            >
              {expandedCards[item.id] ? "Read Less" : "Read More"}
            </p>
          </VerticalTimelineElement>
        ))}
      </VerticalTimeline>
    </div>
  );
};

export default Timeline;
