using System;

namespace thumbnailService.Models;

public partial class JobFullInformation
{
    public JobFullInformation(string name, Guid id, JobStatus status)
    {
        Name = name;
        Id = id;
        Status = status;
    }

    public JobFullInformation(string name, JobStatus status)
    {
        Name = name;
        Id = new Guid();
        Status = status;
    }
}
